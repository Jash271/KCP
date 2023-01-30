import boto3
comprehend_client = boto3.client('comprehend')
 
text = f'Implemented a Microsoft PowerPlatform Application to automate access requests for S/4 systems by reducing manual effort by around 60% Integrated GSAP (SAP ECC system) with a 3rd party tool Hexagon for replacing legacy system to cloud. Analyzed and managed defect management process to ensure no delays in deployment Piloted and built a S4 Role Repository application in Microsoft PowerPlatform integrated with MS SQL server to streamline CRUD operations for role management Enhanced ABAP (Advanced Business Application Programming) reports and scripts to generate netting documents, archive it in OpenText and email user to optimize month end process'
 


def extract_keyword(txt):
    entities = comprehend_client.detect_entities(Text = txt, LanguageCode = 'en')
    return {
        "result":entities
    }

print(extract_keyword(text))