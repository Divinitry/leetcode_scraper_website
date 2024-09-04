from leetscrape import GetQuestion

# search_term = "two-sum"

# question = GetQuestion(titleSlug=f"{search_term}").scrape()

# print(question.title)

def get_leetscrape_data(search_string):
    search_term = search_string
    search_term.replace(" ", "-")
    question = GetQuestion(titleSlug=f"{search_term}").scrape()
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
    
    return(
        search_object
    )
