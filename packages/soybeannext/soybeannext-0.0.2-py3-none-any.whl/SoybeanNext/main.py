import time
from .reader import Reader
from .forward import Forward
def Run():
    r = Reader()  # instantiate class Reader
    s = time.time()
    df = r.readVCF(r"example/missing_examples.vcf")  # get the processed dataframe
    e = time.time()
    print(f"readVCF————{e - s:.2f}")
    s = time.time()
    df_filter, isMissing = r.SNPfilter(df)  # get the filtered dataframe
    e = time.time()
    print(f"SNPfilter————{e - s:.2f}")
    s = time.time()
    index_list, sample_resized = r.one_hot(df_filter)  # convert to one-hot matrix and resize every samples
    e = time.time()
    print(f"one_hot————{e - s:.2f}")
    s = time.time()
    f = Forward(['MG', 'P_DENS'])  # instantiate class Forward
    df = f.forward(index_list, sample_resized, 30)  # predict and get results
    e = time.time()
    print(f"forward————{e - s: .2f}")
    df.to_csv("./result.csv", index=False)

Run()
