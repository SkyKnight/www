for i in News.objects.values('date'):
    month={'year':i['date'].year,'month':i['date'].month}
    if month not in lista5:
        lista5.append(month)

