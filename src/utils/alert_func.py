import sys
sys.path.append('src')


def alert(min_temp,max_temp,actual_temp):
    if(min_temp<actual_temp<max_temp):
        return False
    else:
        return True

def gui_alert(current_temp):
    # Open the file and read its content
    with open("src/frontend/frontend_components.py", "r") as file:
        content = file.read()

    # Find the position where you want to insert the new content
    insertion_point = content.find("#insertion")

    # Insert the new content
    new_content = f"st.toast(f\"Your alert was triggered, details has been sent via Email.\")\n"
    modified_content = content[:insertion_point] + new_content + content[insertion_point:]

    # Write the modified content back to the file
    with open("src/frontend/frontend_components.py", "w") as file:
        file.write(modified_content)
    



