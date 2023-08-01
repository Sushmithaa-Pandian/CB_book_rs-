import pickle
import streamlit as st
import pandas as pd
import requests

def content_based(bookTitle):
    bookTitle=str(bookTitle)

    if bookTitle in dataset["Book-Title"].values:
        rating_count=pd.DataFrame(dataset["Book-Title"].value_counts())
        rare_books=rating_count[rating_count["Book-Title"]<=10].index
        common_books=dataset[~dataset["Book-Title"].isin(rare_books)]

        if bookTitle in rare_books:
            print("No Recommendations for this Book \n ")
        else:
            common_books=common_books.drop_duplicates(subset=["Book-Title"])
            common_books.reset_index(inplace=True)
            common_books["index"]=[i for i in range(common_books.shape[0])]
            targets=["Book-Title","Book-Author","Publisher"]
            common_books["all_features"] = [" ".join(common_books[targets].iloc[i,].values) for i in range(common_books[targets].shape[0])]
            vectorizer=CountVectorizer()
            common_booksVector=vectorizer.fit_transform(common_books["all_features"])
            similarity=cosine_similarity(common_booksVector)
            index=common_books[common_books["Book-Title"]==bookTitle]["index"].values[0]
            similar_books=list(enumerate(similarity[index]))
            similar_booksSorted=sorted(similar_books,key=lambda x:x[1],reverse=True)[1:6]
            books=[]
            for i in range(len(similar_booksSorted)):
                books.append(common_books[common_books["index"]==similar_booksSorted[i][0]]["Book-Title"].item())
            print("Here are books you may like")

            return books


bookss_dict = pickle.load(open('books_dict.pkl','rb'))
bookss=pd.DataFrame("bookss_dict")

st.title('Book Recommender System')
books_list = bookss['Book-Title'].values
selected_book= st.selectbox(books_list)

if st.button('Show Recommendation'):
    books=content_based(selected_book)
    for i in books:
        st.write(i)


