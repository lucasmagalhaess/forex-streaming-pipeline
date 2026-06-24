output "datalake_bucket_name" {
  description = "Nome do bucket S3 do Data Lake"
  value       = aws_s3_bucket.datalake.bucket
}

output "kinesis_stream_name" {
  description = "Nome do Kinesis Data Stream"
  value       = aws_kinesis_stream.forex_stream.name
}

output "kinesis_stream_arn" {
  description = "ARN do Kinesis Data Stream"
  value       = aws_kinesis_stream.forex_stream.arn
}

output "emr_application_id" {
  description = "ID da aplicação EMR Serverless"
  value       = aws_emrserverless_application.spark.id
}

output "lambda_role_arn" {
  description = "ARN da role IAM do Lambda"
  value       = aws_iam_role.lambda_role.arn
}

output "emr_role_arn" {
  description = "ARN da role IAM do EMR"
  value       = aws_iam_role.emr_role.arn
}