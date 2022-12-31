"""Various helper functions dealing with user results."""


def by_score(albums):
    """Sort albums by score (descending)."""
    temp = []
    output = []

    for i in albums:
        temp.append((i, albums[i][0], albums[i][1]))

    temp.sort(key=lambda x: (-x[1], x[0].split(' - ')[0], x[0].split(' - ')[1]))
    for i in temp:
        output.append([(str(i[1]) + '/10: ' + i[0].lower()), i[2]])
    return output


def by_artist(albums):
    """Sort albums alphabetically by artist."""
    output = albums.copy()
    output.sort(key=lambda x: x[0].split(': ')[1])
    return output


def get_unscored_albums(albums):
    """Sort unscored albums alphabetically by artist."""
    output = []
    for i in albums:
        if i[1] < 0:
            output.append([i[0].lower(), i[2]])
    output.sort(key=lambda x: (x[0].split(' - ')[0], x[0].split(' - ')[1]))
    return output


def all_by_score(albums):
    """Sort all albums by score."""
    temp = sorted(albums.items(), key=lambda x: (-x[1], x[0]))
    output = []
    for i in temp:
        output.append([str(i[1]) + '/10: ' + i[0]])
    return output


def all_by_artist(albums):
    """Sort all albums by artist."""
    temp = sorted(albums.items(), key=lambda x: (x[0], -x[1]))
    output = []
    for i in temp:
        output.append([str(i[1]) + '/10: ' + i[0]])
    return output


def get_score_data(albums):
    """Return data for bar chart of scores distribution."""
    data = {
        "10s": 0,
        "9s": 0,
        "8s": 0,
        "7s": 0,
        "6s": 0,
        "5s": 0,
        "4s": 0,
        "3s": 0,
        "2s": 0,
        "1s": 0,
        "0s": 0,
    }

    for i in albums:
        if albums[i][0] == 10:
            data["10s"] += 1
        elif albums[i][0] == 9:
            data["9s"] += 1
        elif albums[i][0] == 8:
            data["8s"] += 1
        elif albums[i][0] == 7:
            data["7s"] += 1
        elif albums[i][0] == 6:
            data["6s"] += 1
        elif albums[i][0] == 5:
            data["5s"] += 1
        elif albums[i][0] == 4:
            data["4s"] += 1
        elif albums[i][0] == 3:
            data["3s"] += 1
        elif albums[i][0] == 2:
            data["2s"] += 1
        elif albums[i][0] == 1:
            data["1s"] += 1
        elif albums[i][0] == 0:
            data["0s"] += 1

    return data


def get_all_score_data(albums):
    """Return data for bar chart of scores distribution."""
    data = {
        "10s": 0,
        "9s": 0,
        "8s": 0,
        "7s": 0,
        "6s": 0,
        "5s": 0,
        "4s": 0,
        "3s": 0,
        "2s": 0,
        "1s": 0,
        "0s": 0,
    }
    for value in albums.values():
        if value == 10:
            data["10s"] += 1
        elif value == 9:
            data["9s"] += 1
        elif value == 8:
            data["8s"] += 1
        elif value == 7:
            data["7s"] += 1
        elif value == 6:
            data["6s"] += 1
        elif value == 5:
            data["5s"] += 1
        elif value == 4:
            data["4s"] += 1
        elif value == 3:
            data["3s"] += 1
        elif value == 2:
            data["2s"] += 1
        elif value == 1:
            data["1s"] += 1
        elif value == 0:
            data["0s"] += 1

    return data


def get_average(score_data):
    sum = score_data["10s"] * 10
    sum += score_data["9s"] * 9
    sum += score_data["8s"] * 8
    sum += score_data["7s"] * 7
    sum += score_data["6s"] * 6
    sum += score_data["5s"] * 5
    sum += score_data["4s"] * 4
    sum += score_data["3s"] * 3
    sum += score_data["2s"] * 2
    sum += score_data["1s"] * 1
    sum += score_data["0s"] * 0

    total = 0
    for value in score_data.values():
        total += value

    return round((sum / total), 2)


def get_score_path(average):
    """Return the appropriate score png based on average score."""
    if 0 <= average < .33:
        return 'light0.png'
    elif .33 <= average < .66:
        return 'decent0.png'
    elif .66 <= average < 1:
        return 'strong0.png'

    elif 1 <= average < 1.33:
        return 'light1.png'
    elif 1.33 <= average < 1.66:
        return 'decent1.png'
    elif 1.66 <= average < 2:
        return 'strong1.png'

    elif 2 <= average < 2.33:
        return 'light2.png'
    elif 2.33 <= average < 2.66:
        return 'decent2.png'
    elif 2.66 <= average < 3:
        return 'strong2.png'

    elif 3 <= average < 3.33:
        return 'light3.png'
    elif 3.33 <= average < 3.66:
        return 'decent3.png'
    elif 3.66 <= average < 4:
        return 'strong3.png'

    elif 4 <= average < 4.33:
        return 'light4.png'
    elif 4.33 <= average < 4.66:
        return 'decent4.png'
    elif 4.66 <= average < 5:
        return 'strong4.png'

    elif 5 <= average < 5.33:
        return 'light5.png'
    elif 5.33 <= average < 5.66:
        return 'decent5.png'
    elif 5.66 <= average < 6:
        return 'strong5.png'

    elif 6 <= average < 6.33:
        return 'light6.png'
    elif 6.33 <= average < 6.66:
        return 'decent6.png'
    elif 6.66 <= average < 7:
        return 'strong6.png'

    elif 7 <= average < 7.33:
        return 'light7.png'
    elif 7.33 <= average < 7.66:
        return 'decent7.png'
    elif 7.66 <= average < 8:
        return 'strong7.png'

    elif 8 <= average < 8.33:
        return 'light8.png'
    elif 8.33 <= average < 8.66:
        return 'decent8.png'
    elif 8.66 <= average < 9:
        return 'strong8.png'

    elif 9 <= average < 9.33:
        return 'light9.png'
    elif 9.33 <= average < 9.66:
        return 'decent9.png'
    elif 9.66 <= average < 10:
        return 'strong9.png'

    elif 10 <= average:
        return '10.png'

