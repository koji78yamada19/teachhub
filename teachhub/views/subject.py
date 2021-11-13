from django.shortcuts import render
from teachhub.models import Subject, SchoolClassification, SubjectArea
from django.contrib.auth.decorators import login_required


@login_required
def get_subjects(request, classification_id, area_id):
    if request.method == 'GET':
        classification = SchoolClassification.objects.get(id=classification_id)
        subject_area = SubjectArea.objects.get(
            id=area_id, school_classification=classification)
        subjects = Subject.objects.filter(
            subject_area=subject_area, school_classification=classification).order_by('id')
        context = {
            "classification_name": classification.name,
            'subject_area_name': subject_area.name,
            'subject_area_id': subject_area.id,
            'subjects': subjects
        }
        return render(
            request,
            'teachhub/subject_list.html',
            context
        )
