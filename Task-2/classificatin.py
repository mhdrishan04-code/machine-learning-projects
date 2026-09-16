from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score

iris = load_iris()
X = iris.data
Y = iris.target

print("iris dataset loaded successfully")
print("number of samples:", len(X))
print("number of features:", X.shape[1])
print("Classes:", iris.target_names)

X_train, X_test, y_train, y_test = train_test_split(
    X, Y, test_size=0.2, random_state=42, stratify=Y
)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)

y_pred = knn.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)
f1 = f1_score(y_test, y_pred, average="weighted")

print("\nAccuracy score:", accuracy)
print("\nConfusion Matrix:")
print(cm)
print("\nF1 Score:", f1)
