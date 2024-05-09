import uuid
import os

# from appointment_booking.models.generic_picture import Generic_Picture


# Custom function to generate the upload path
def get_upload_path(instance: "Generic_Picture", filename: str) -> str:
    """
    Returns the upload path for the image based on the content type and object ID.

    Args:
        instance (Generic_Picture): The instance of the model.
        filename (str): The original filename of the uploaded file.

    Returns:
        str: The constructed upload path.
    """
    # Split the filename to get the base name and extension
    base_name, ext = os.path.splitext(filename)

    # Generate a 6-character unique identifier
    short_uuid = str(uuid.uuid4())[:6]

    # Construct the new unique filename
    unique_filename = f"{base_name}_{short_uuid}{ext}"

    # Determine the associated content type and set the appropriate path
    content_type = instance.content_type.model

    if content_type == "service":
        return f"photos/services/{instance.object_id}/{unique_filename}"
    elif content_type == "user":
        return f"photos/users/{instance.object_id}/{unique_filename}"
    else:
        # Default to a generic path if content type is unknown
        return f"photos/others/{unique_filename}"
