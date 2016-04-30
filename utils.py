monthList = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

def dateFunc(tree):
    dates = []
    months = []
    for tags in tree:
        if type(tags) is not tuple:
            if tags.label() == 'DATES':
                d, m = dateFund(tags)
                dates = dates+d
                month = month+m
        if tags[1] == 'CD':
            date = ''.join(x for x in tags[0] if x.isdigit())
            dates.append(int(date))
        elif tags[1] not in ['CD',':', ',', '.', 'TO', 'IN', 'AND', 'CC']:
            months.append(tags[0])
    return dates,months

def dateMonth(dates, months):
    if len(dates) == 1:
        from_date = dates[0]
        if dates[0] >= 30:
            to_date = 1
        else:
            from_date = dates[0] + 1
    else:
        from_date = dates[0]
        to_date = dates[-1]
    modifiedMonths = []
    for i, m in enumerate(months):
        for mcount, mon in enumerate(monthList):
            if m.lower() in mon.lower():
                modifiedMonths.append(mcount+1)
                break
    if len(modifiedMonths) > 0:
        if len(modifiedMonths) == 1:
            from_month = to_month = modifiedMonths[0]
        else:
            modifiedMonths.sort()
            from_month = modifiedMonths[0]
            to_month = modifiedMonths[-1]
    else:
        from_month = datetime.datetime.now().month
        to_month = datetime.datetime.now().month
    return from_date, from_month, to_date, to_month
