from django.shortcuts import render
from teachhub.models import Subject, SchoolClassification, SubjectArea
from django.contrib.auth.decorators import login_required


@login_required
def get_subjects(request, classification_id, area_id):
    if request.method == 'GET':
        print(classification_id)
        print(area_id)
        classification = SchoolClassification.objects.get(id=classification_id)
        subject_area = SubjectArea.objects.get(id=area_id)
        print('subject_area')
        print(subject_area)
        tmp_subjects = Subject.objects.filter(
            subject_area=subject_area).order_by('id')
        print('tmp_subjects')
        print(tmp_subjects)
        subjects = []
        for subject in tmp_subjects:
            subject_name = subject.name.split('-')[1]
            subjects.append({
                'id': subject.id,
                'name': subject_name
            })
        context = {
            "classification_name": classification.name,
            'subject_area_name': subject_area.name.split('-')[1],
            'subject_area_id': subject_area.id,
            'subjects': subjects
        }
        print('context')
        print(context)
        return render(
            request,
            'teachhub/subject_list.html',
            context
        )
