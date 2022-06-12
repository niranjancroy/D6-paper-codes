import yt 
import time


filename = input("Enter filename for stats: \n")
ds = yt.load(filename)
print("printing stats.........")
time.sleep(1)
ds.print_stats()

print("printing field list......")
time.sleep(1)
for i in sorted(ds.field_list):
    print(i)

print("printing derived field list......")
time.sleep(1)
for i in sorted(ds.derived_field_list):
    print(i)

