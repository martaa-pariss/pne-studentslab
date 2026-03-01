temperatures = [15.5, 17.2, 14.8, 16.0, 18.3, 20.1, 19.5]

print("The temperature on wednesday was:", temperatures[2], "Degrees celsius")
print("The maximum temperature registered is:", max(temperatures), "Degrees celsius")
print("The minimum temperature registered is", min(temperatures), "Degrees celsius")

average_temp = sum(temperatures)/len(temperatures)
print("The average temperature for this week is:", round(average_temp), "Degrees celsius")

count_of_days_above_17 = 0
for temp in temperatures:
    if temp > 17:
        count_of_days_above_17 += 1
print("The number of days above 17 is:", count_of_days_above_17)
ordered_list = sorted(temperatures)
print("The sorted values of the list of temperatures is:", ordered_list)

