import pandas as pd
import random

data = []

careers = ["Engineering","Doctor","Lawyer","Arts"]

for i in range(1000):

    R = random.randint(3,15)
    I = random.randint(3,15)
    A = random.randint(3,15)
    S = random.randint(3,15)
    E = random.randint(3,15)
    C = random.randint(3,15)

    if R > 12:
        career = "Engineering"
    elif S > 12:
        career = "Doctor"
    elif E > 12:
        career = "Lawyer"
    else:
        career = "Arts"

    data.append([R,I,A,S,E,C,career])

df = pd.DataFrame(data, columns=["R","I","A","S","E","C","Career"])

df.to_csv("career_dataset.csv", index=False)

print("Dataset Created")