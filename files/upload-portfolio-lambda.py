import boto3
from botocore.client import Config
import StringIO
import zipfile
    
def lambda_handler(event, context):
    sns = boto3.resource('sns')
    topic = sns.Topic("arn:aws:sns:ca-central-1:245541724377:deployPortfolioTopic")
    location = {
        "bucketName": 'portfoliobuild.raekonn.com',
        "objectKey": 'portfoliobuild.zip'
    }
    try:
        job = event.get("CodePipeline.job")
        print "Jobs are: ", job
        if job:
            for artifact in job["data"]["inputArtifacts"]:
                print "Artifacts are: ", artifact
                if artifact["name"] == "BuildArtif":
                    location = artifact["location"]["s3Location"]
                    print "BuildArtif successful"
        else:
            print "BuildArtif failed!"
                
        print "Building portfolio from " + str(location)
        
        s3 = boto3.resource('s3', config=Config(signature_version='s3v4'))
        
        portfolio_bucket = s3.Bucket('portfolio.raekonn.com')
        build_bucket = s3.Bucket(location["bucketName"])
        
        portfolio_zip = StringIO.StringIO()
        build_bucket.download_fileobj(location["objectKey"], portfolio_zip)
        
        with zipfile.ZipFile(portfolio_zip) as myzip:
        	for nm in myzip.namelist():
        		obj = myzip.open(nm)
        		portfolio_bucket.upload_fileobj(obj, nm)
        		portfolio_bucket.Object(nm).Acl().put(ACL='public-read')
        
        print "Job Done!"
        topic.publish(Subject="Portfolio Deployed", Message="Portfolio deployed successfully!")
        if job:
            codepipeline = boto3.client('codepipeline')
            codepipeline.put_job_success_result(jobId=job["id"])
    except:
        topic.publish(Subject="Portfolio  Deployment Failed", Message="Portfolio was not deployed successfully!")
    
    return 'Hello from Lambda'