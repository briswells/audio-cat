import requests

#before doing this possibly look if file is already tagged?

def title_search(title):
    resp = requests.get("https://www.googleapis.com/books/v1/volumes?q=" + title)
    if resp.status_code != 200:
        raise ApiError('Cannot lookup book title: {}'.format(resp.status_code))
        exit()
    response = resp.json()
    results = response["items"] #returns a list of book info dictionaries
    return results

def print_titles(results, start, finish):
    for index in range (start, finish+1):
        if results[index]["volumeInfo"]["authors"]:
            authors = get_authors(results[index]["volumeInfo"]["authors"])
        print(f'  {index+1}: {results[index]["volumeInfo"]["title"]} {authors} {results[index]["volumeInfo"]["publishedDate"]}')

def book_select(results):
    print("Based on output filename top 3 book results are:")
    print_titles(results, 0,2)
    print("  4: More options")
    print("  5: Skip gathering metadata")
    selection = input("Enter option: ")
    if int(selection) == 5:
        return None
    elif int(selection) == 4:
        print_titles(results, 0, 9)
        print("  11: Skip gathering metadata")
        selection = input("Enter option: ")
        if int(selection) == 11:
            return None
        else:
            index = int(selection) - 1
            return results[index]["volumeInfo"]

def get_authors(list):
    if len(list) == 1:
        return list[0]
    else:
        authors = ""
        for index in range(0,len(list)):
            authors += list[index]
            if index + 2 <= len(list):
                authors += ", "
            if index + 2 == len(list):
                authors += "and "
    return authors
