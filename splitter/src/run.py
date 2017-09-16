from ml.transaction_classifier import Classifier
if __name__ == "__main__":
    clf = Classifier()

    trans_descriptions =["Rema1000", "Elkjøp", "Uttak"]
    predictions = clf.predict(trans_descriptions)

    print(predictions)