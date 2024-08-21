def coin_change(coins, amount):
    # Initialize the table with a value greater than the possible minimum coins needed
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0  # Base case: 0 coins needed to make amount 0

    for coin in coins:
        print("\n\n\ncoin: ", coin)

        for x in range(coin, amount + 1):
            print("This is x:", x)
            dp[x] = min(dp[x], dp[x - coin] + 1)
            print("This is dp[x]:", dp[x])

    return dp[amount] if dp[amount] != float('inf') else -1

# Example usage
coins = [1, 2, 5]
amount = 11
print(coin_change(coins, amount))  # Output: 3

