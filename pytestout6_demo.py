import pytestout6
import sys
import random
import time
from tqdm import tqdm

def complete_lab(client, user_id, default_version_id, resource_id):
    create_exam_response = client.create_exam(
        user_id, 
        default_version_id,
    )
    print(resource.get_index())
    exam_session_id = create_exam_response.get_exam_session_id()
    exam_time = random.randrange(300, 600)
    
def complete_quiz(client, user_id, default_version_id, resource_id):
    create_exam_response = client.create_exam(
        user_id, 
        default_version_id,
        resource_id
    )
    print(resource.get_index())    
    exam_session_id = create_exam_response.get_exam_session_id()
    exam_time = random.randrange(127, 250)

    submit_result_request = pytestout6.SubmitResultRequest(
        user_profile_id = user_id,
        resource_id = resource_id,
        resource_type = 4,
        resource_sub_type = 4,
        group_id = default_version_id,
        points_scored = random.randrange(8, 10 + 1),
        points_possible = 10,
        passed = True,
        seconds_in_resource = exam_time,
        response_details = exam_session_id,
        exam_session_id = exam_session_id,
    )

    print("Sleeping for " + str(exam_time))
    for i in tqdm(range(exam_time)):
        time.sleep(1)
                    
    submit_result_response = client.submit_result(
        user_id,
        submit_result_request,
    )

# Input
username = input("Enter Username: ")
password = input("Enter Password: ")

# Create a client
client = pytestout6.Client()

# Login
login_response = client.login(username, password)

# Check if succesful
if not login_response.is_successful():
	sys.exit("failed to log in")

print("hacking the main frame")
time.sleep(3)	
# Get the user id. This is used for some requests.
user_id = login_response.get_user_id()
	
# Get classes
classes_response = client.get_activated_products_and_classes(user_id)

for product in classes_response.get_activated_products():    
    default_version = product.get_default_available_version()      
    default_product_version = product.get_default_product_version()
    
    if default_version is None:
        sys.exit("failed to locate default version")
        
    if default_product_version is None:
        sys.exit("failed to locate default product version")
        
    outline = client.get_outline(
        major_version = default_product_version.get_major_version(), 
        minor_version = default_product_version.get_minor_version(),
        patch_version = default_product_version.get_patch_version(),
        locale = product.get_locale(),
        href = default_product_version.get_outline_href()
    )
    
    default_version_id = product.get_default_version_id()
    
    resource_map = client.get_resource_map(
        default_version_id, 
        default_product_version.get_patch_version()
    )
    
    all_sections = outline.get_all_sections()
         
    chapter = input("What chapter do you want to use? \n")
    labs = int(input("How many labs do you want to do? \n"))
    quiz = int(input("How many quizes do you want to do? \n"))
    quizCount = 0
    labCount = 0
    
    assments = []
    for section in all_sections:
        resources = section.get_resources()
        for resource in resources:
            resource_map_entry = resource_map.get(resource.get_href())
            
            if resource_map_entry is not None and (resource_map_entry.is_sim() or resource_map_entry.is_exam()):
                assments.append((resource, resource_map_entry))
                
    for (resource, resource_map_entry) in assments:
        
        resource_id = resource_map_entry.get_resource_id()
        if resource.get_index().split(".")[0] == chapter and resource_map_entry.is_sim() and labCount < labs:
            complete_lab(client, user_id, default_version_id, resource_id)
            labCount += 1
    
    for (resource, resource_map_entry) in assments:
        
        resource_id = resource_map_entry.get_resource_id()
        if resource.get_index().split(".")[0] == chapter and resource_map_entry.is_exam() and quizCount < quiz:
            complete_quiz(client, user_id, default_version_id, resource_id)            
            quizCount += 1
            
