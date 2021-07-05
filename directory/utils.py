import csv
import os
import shutil
import uuid
import zipfile

from django.conf import settings
from django.core.files import File

from directory.models import Teacher, Subject


def normalize_string(value: str) -> str:
    """
    Converts ' String   ' to 'string'
    """
    return value.lower().strip()


def save_file_temporarily(in_memory, file_path: str) -> None:
    """
    Saves an in-memory file on disk
    """
    with open(file_path, 'wb+') as destination:
        for chunk in in_memory.chunks():
            destination.write(chunk)


def import_teachers(*args, **kwargs):
    # Save files on disk
    data_csv_file = kwargs.get('data_csv_file')
    images_zip_file = kwargs.get('images_zip_file')

    temp_path = os.path.join(settings.MEDIA_ROOT, os.path.join('temp', uuid.uuid4().hex[:6]))
    images_path = os.path.join(temp_path, 'images')
    os.makedirs(temp_path)
    os.makedirs(images_path)
    csv_path = os.path.join(temp_path, 'data.csv')
    zip_path = os.path.join(temp_path, 'images.zip')
    save_file_temporarily(data_csv_file, csv_path)
    save_file_temporarily(images_zip_file, zip_path)

    # Extract Zip File
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(images_path)

    # Read CSV File
    with open(csv_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader, None)
        for row in csv_reader:
            try:
                if row[0] == '':
                    continue
                # Extract Profile Image
                image_path = os.path.join(images_path, row[2].lower())
                if not os.path.exists(image_path):
                    image_path = None
                # Create Teacher Object
                teacher = Teacher.objects.create(
                    first_name=row[0],
                    last_name=row[1],
                    email_address=row[3],
                    phone_number=row[4],
                    room_number=row[5],
                )
                # Save Image
                if image_path:
                    print("Image Path", image_path)
                    teacher.profile_picture.save(
                        os.path.basename(image_path),
                        File(open(image_path, 'rb'))
                    )
                # Extract Subjects
                subject_names = row[6].split(",")
                subject_names = map(normalize_string, subject_names)  # Normalize them
                subject_names = list(set(subject_names))  # Remove Duplicates
                # Create Relations
                teacher.subjects.add(
                    *[Subject.objects.get_or_create(title=subject_name)[0].id for subject_name in subject_names]
                )
                teacher.save()

            except Exception as e:
                print(e)

    shutil.rmtree(temp_path)
