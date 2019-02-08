import skeleton as sk

dp = sk.Cmake("demo project")

print("\n====>empty project\n")
print(dp)

tg = dp.add_target("client")
tg.add_file("src/main.c")

print("\n====>single target empty project\n")
print(dp)
