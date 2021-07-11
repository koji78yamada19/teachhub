from django.shortcuts import render
from teachhub.models import SubjectArea, SchoolClassification
from django.contrib.auth.decorators import login_required

# 教科の一覧


@login_required
def get_subject_areas(request):
    classifications = SchoolClassification.objects.all().order_by('id')
    areas_with_classifications = []
    for classification in classifications:
        subject_areas = SubjectArea.objects.filter(
            school_classification=classification).order_by('id')
        areas = []
        for area in subject_areas:
            area_name = area.name.split('-')[1]
            areas.append({
                'id': area.id,
                'name': area_name
            })
        areas_with_classifications.append({
            'classification': classification,
            'areas': areas
        })
    context = {
        'areas_with_classifications': areas_with_classifications
    }
    print('context')
    print(context)
    return render(request, 'teachhub/subject_area_list.html', context)
