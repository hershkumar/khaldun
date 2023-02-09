# Testing `khaldun`
## Hersh Kumar

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum fringilla consectetur massa eu condimentum. Proin ullamcorper odio nec lobortis tincidunt. Maecenas eget nisi vitae massa bibendum vulputate ac ut ante. Nullam accumsan odio et laoreet bibendum. Sed in pellentesque velit, vel porttitor elit. Sed sed magna et ex facilisis hendrerit vel vitae magna. Sed dui nunc, pretium vel accumsan id, cursus fermentum enim. Phasellus pellentesque erat eros. Maecenas tellus sem, ornare a sagittis id, varius id nulla. Nunc auctor magna ut tristique hendrerit. Etiam elementum metus ut ligula aliquam consequat. Etiam augue diam, mattis pretium lectus et, ornare accumsan est. Nunc commodo sem sed consequat lacinia. Aliquam erat volutpat. Duis tristique nisl nunc, eu porttitor quam ornare non.

<!---khaldun type="input" name="python test" language="python"--->
```python
print("Hello World!")
for i in range(5):
	print(i)
print("Goodbye!")
```

This is the output of the above Python code:
<!--- khaldun type="output" name="python test" --->	

```
Hello World!
0
1
2
3
4
Goodbye!

```


<!---khaldun type="input" name="haskell test" language="haskell"--->
```haskell
-- function that takes a list and reverses it 
rev :: [a] -> [a]

rev [] = []
rev (x:xs) = rev xs ++ [x]

-- recursive factorial function
factorial :: Integer -> Integer

factorial 1 = 1
factorial n = n * factorial (n-1)


-- counts the length of a list 
len :: [a] -> Integer
len [] = 0
len (x:xs) = len xs + 1

-- predicate to check if integer is even 
isEven :: Integer -> Bool
isEven x = if mod x 2 == 0 then True else False

-- function that keeps only even numbers in list
keepeven :: [Integer] -> [Integer]
keepeven [] = []
keepeven (x:xs) = if isEven x then x : keepeven xs else keepeven xs


-- add up numbers in list 
sumlist :: [Integer] -> Integer
sumlist [] = 0
sumlist (x:xs) = sumlist xs + x

main = do 
    print $ sumlist [1,2,3,4,5,6]
    print $ rev [1,2,3,4,5,6]
```
The output of the above haskell code is shown below:
<!--- khaldun type="output" name="haskell test" --->

```
21
[6,5,4,3,2,1]

```



<!---khaldun type="input" name="pythonfn" language="python" --->
```python
def testing_fn(x):
	return x + 1

for i in range(5):
	print(testing_fn(i))
print("Goodbye!")
```
python output:
<!---khaldun type="output" name="pythonfn" --->

```
1
2
3
4
5
Goodbye!

```


