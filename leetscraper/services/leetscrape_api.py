from leetscrape import GetQuestion

def get_leetscrape_data(search_string):
    if not isinstance(search_string, str):
        print(f"Error: Received non-string input: {search_string}")
        return {"error": "Invalid input"}
    
    search_term = search_string.strip().replace(" ", "-")
    
    try:
        question = GetQuestion(titleSlug=search_term).scrape()

        if not question:
            return {"error": "No question data found"}

        search_object = {
            'QID': question.QID,
            'title': question.title,
            'titleSlug': question.titleSlug,
            'difficulty': question.difficulty,
            'Hints': question.Hints,
            'Companies': question.Companies,
            'topics': question.topics,
            'SimilarQuestions': question.SimilarQuestions,
            'Code': question.Code,
            'Body': question.Body,
            'isPaidOnly': question.isPaidOnly,
        }
        return search_object

    except Exception as e:
        print(f"Error scraping data: {str(e)}")
        return {"error": "Failed to fetch data"}
