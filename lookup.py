import requests

def title_search(title):
    resp = requests.get("https://www.googleapis.com/books/v1/volumes?q=" + title)
    if resp.status_code != 200:
        raise ApiError('Cannot lookup book title: {}'.format(resp.status_code))
        exit()
    response = resp.json()
    results = response["items"] #returns a list of book info dictionaries
    # print(results[2])
    # exit()
    return results

def print_titles(results, start, finish):
    for index in range (start, finish+1):
        authors = ""
        if results[index]["volumeInfo"]["authors"]:
            for author in results[index]["volumeInfo"]["authors"]:
                authors += author + " "
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
        else
            index = int(selection) - 1
            return results[index]
