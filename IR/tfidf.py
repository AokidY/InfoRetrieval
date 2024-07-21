import math


# W(t,d)= (1+log(tft,d)) x log(N/df(t))
def tfidf_value(total_documents, inverted_index):
    document_frequency = {}
    for single_word, file_path in inverted_index.items():
        # We can obtain the number of files having this word
        # the number of files in which this single word has appeared is saved in 'document_frequency'
        document_frequency[single_word] = len(file_path)
    # print(document_frequency)
#
#     # Calculate IDF
    inverse_document_frequency = {}
    for single_word, df in document_frequency.items():
        idf = math.log(total_documents / (df))
        inverse_document_frequency[single_word] = idf

    for single_word, document_info in inverted_index.items():
        for document, frequency in document_info.items():
            frequency_val = 1 + math.log(frequency)
            # the tf_idf score in this specific json file
            tf_idf_score = frequency_val * inverse_document_frequency[single_word]
            inverted_index[single_word][document] = tf_idf_score
    # print(inverse_document_frequency)
    print(inverted_index)
    # print(total_documents)


