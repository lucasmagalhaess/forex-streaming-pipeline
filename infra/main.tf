terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

# ── S3 — Data Lake (Bronze + Silver + Gold) ──────────────────────────────────
resource "aws_s3_bucket" "datalake" {
  bucket = "${var.project_name}-datalake-${var.environment}"

  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}

resource "aws_s3_bucket_versioning" "datalake" {
  bucket = aws_s3_bucket.datalake.id
  versioning_configuration {
    status = "Enabled"
  }
}

# ── IAM Role — Lambda ─────────────────────────────────────────────────────────
resource "aws_iam_role" "lambda_role" {
  name = "${var.project_name}-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })

  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}

resource "aws_iam_role_policy" "lambda_policy" {
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = ["s3:GetObject", "s3:PutObject", "s3:ListBucket"]
        Resource = [
          aws_s3_bucket.datalake.arn,
          "${aws_s3_bucket.datalake.arn}/*"
        ]
      },
      {
        Effect   = "Allow"
        Action   = ["secretsmanager:GetSecretValue"]
        Resource = "arn:aws:secretsmanager:us-east-1:*:secret:forex-pipeline/*"
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })
}

# ── Kinesis Data Stream ───────────────────────────────────────────────────────
resource "aws_kinesis_stream" "forex_stream" {
  name             = "${var.project_name}-stream"
  shard_count      = 1
  retention_period = 24

  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}

# ── EMR Serverless ────────────────────────────────────────────────────────────
resource "aws_emrserverless_application" "spark" {
  name          = "${var.project_name}-spark"
  release_label = "emr-6.15.0"
  type          = "SPARK"

  maximum_capacity {
    cpu    = "4 vCPU"
    memory = "16 GB"
  }

  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}

# ── IAM Role — EMR Serverless ─────────────────────────────────────────────────
resource "aws_iam_role" "emr_role" {
  name = "${var.project_name}-emr-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "emr-serverless.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy" "emr_policy" {
  role = aws_iam_role.emr_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "s3:GetObject",
        "s3:PutObject",
        "s3:ListBucket",
        "s3:DeleteObject"
      ]
      Resource = [
        aws_s3_bucket.datalake.arn,
        "${aws_s3_bucket.datalake.arn}/*"
      ]
    }]
  })
}