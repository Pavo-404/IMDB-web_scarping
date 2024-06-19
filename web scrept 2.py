from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

# Downloading IMDb top 250 movie's data
url = 'http://www.imdb.com/chart/top'
response = requests.get(url).
soup = BeautifulSoup(response.text, "html.parser")
movies = soup.select('td.titleColumn')
crew = [a.attrs.get('title') for a in soup.select('td.titleColumn a')]
ratings = [float(b.attrs.get('data-value')) for b in soup.select('td.posterColumn span[name=ir]')]

# Check if we are getting the correct number of movies, crew, and ratings
print(f"Number of movies found: {len(movies)}")
print(f"Number of crew found: {len(crew)}")
print(f"Number of ratings found: {len(ratings)}")

# Create an empty list for storing movie information
movie_list = []

# Iterating over movies to extract each movie's details
for index in range(0, len(movies)):
    # Separating movie into: 'place', 'title', 'year'
    movie_string = movies[index].get_text().strip()
    movie_string = re.sub('\s+', ' ', movie_string)  # Remove extra spaces
    title_search = re.search('(?<=\d\.\s)(.*)(?=\(\d{4}\))', movie_string)
    movie_title = title_search.group(1).strip() if title_search else ''
    year = re.search('\((.*?)\)', movie_string).group(1)
    place = re.search('^\d+', movie_string).group()
    data = {
        "place": place,
        "movie_title": movie_title,
        "rating": ratings[index],
        "year": year,
        "star_cast": crew[index],
    }
    movie_list.append(data)

# Check if the movie_list is populated correctly
print(f"Number of movies parsed: {len(movie_list)}")
for movie in movie_list[:5]:  # Print first 5 movies as a sample
    print(f"{movie['place']} - {movie['movie_title']} ({movie['year']}) - Starring: {movie['star_cast']} - Rating: {movie['rating']}")

# Saving to a CSV file
df = pd.DataFrame(movie_list)
df.to_csv('imdb_top_250_movies.csv', index=False)
print("CSV file has been saved successfully.")
