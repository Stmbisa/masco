from datetime import date

def footer(request):
    current_date = date.today()
    current_year = current_date.year
    return {'current_date': current_date, 'current_year': current_year}