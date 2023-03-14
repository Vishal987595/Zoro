def compute():
	ans = sum(x for x in range(1000) if (x % 3 == 0 or x % 5 == 0))
	return str(ans)


if __name__ == "__main__":
	print(compute())
	
a1 = 1000//3
a2 = 1000//5
a3 = 1000//15

print(a1*(a1+1)/2*3 + a2*(a2+1)/2*5 - a3*(a3+1)/2*15)