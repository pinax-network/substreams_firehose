
# EOS Resources

## `.rex` (REX Resource Exchange)

### `.state`

- [x] `.rexpool`

    <details>

    ```js
    {
        "total_lent": 3006004.5507, // total amount of CORE_SYMBOL in open rex_loans
        "total_unlent": 49428573.1574, // total amount of CORE_SYMBOL available to be lent (connector),
        "total_rent": 3478.0901, // fees received in exchange for lent  (connector),
        "total_lendable": 52434577.7081, // total amount of CORE_SYMBOL that have been lent (total_unlent + total_lent),
        "total_rex": 517222889551.6919, // total number of REX shares allocated to contributors to total_lendable,
        "namebid_proceeds": 0, // the amount of CORE_SYMBOL to be transferred from namebids to REX pool,
        "loan_num": 500607 // increments with each new loan
    }
    ```

    </details>

- [x] `.rexretpool`

    <details>

    ```js
    {
        "last_dist_time": "2022-10-01T05:40:00", // the last time proceeds from renting, ram fees, and name bids were added to the rex pool
        "pending_bucket_time": "2022-10-01T12:00:00", // timestamp of the pending 12-hour return bucket
        "oldest_bucket_time": "2022-09-01T12:00:00", // cached timestamp of the oldest 12-hour return bucket
        "pending_bucket_proceeds": 163198, // proceeds in the pending 12-hour return bucket
        "current_rate_of_increase": 24067, // the current rate per dist_interval at which proceeds are added to the rex pool
        "proceeds": 49371744 // the maximum amount of proceeds that can be added to the rex pool at any given time
    }
    ```
    </details>

### `.actions`

- [x] `.powerup`
    <details>

    ```js
    {
        "cpu_frac": 635429833093, // fraction of cpu (100% = 10^15) managed by this market
        "net_frac": 27497451847, // fraction of net (100% = 10^15) managed by this market
        "actions": 315
    }
    ```
    Powerup NET and CPU resources by percentage
    </details>

- [x] `.powupresult`
    <details>

    ```js
    {
        "fee": 4.289700000000008, // powerup fee amount
        "powup_cpu": 242617351084, // amount of powup CPU tokens
        "powup_cpu_price": 5837903.778625954,
        "powup_net": 2624742481, // amount of powup NET tokens
        "actions": 315
    }
    ```
    The action `powupresult` is a no-op.
    It is added as an inline convenience action to `powerup` reservation.
    This inline convenience action does not have any effect, however, its data includes the result of the parent action and appears in its trace.
    </details>

- [x] `.deposit`
    <details>

    ```js
    {
        "amount": 7317.905500000001, // tokens to be deposited.
        "actions": 8
    }
    ```

    Deposit to REX fund action. Deposits core tokens to user REX fund. All proceeds and expenses related to REX are added to or taken out of this fund. An inline transfer from 'owner' liquid balance is executed. All REX-related costs and proceeds are deducted from and added to 'owner' REX fund, with one exception being buying REX using staked tokens.
    </details>

- [x] `.withdraw`

    <details>

    ```js
    {
        "amount": 197.3181, // amount of tokens to be withdrawn.
        "actions": 8
    }
    ```
    Withdraw from REX fund action, withdraws core tokens from user REX fund.
    </details>

- [x] `.buyrex`

    <details>

    ```js
    {
        "price": 0.00010137714081746883,
        "amount": 7317.905500000001, // amount of tokens taken out of 'from' REX fund.
        "actions": 8
    }
    ```
    Buyrex action, buys REX in exchange for tokens taken out of user's REX fund by transferring core tokens from user REX fund and converts them to REX stake. By buying REX, user is lending tokens in order to be rented as CPU or NET resources.

    @pre A voting requirement must be satisfied before action can be executed.
    @pre User must vote for at least 21 producers or delegate vote to proxy before buying REX.

    @post User votes are updated following this action.
    @post Tokens used in purchase are added to user's voting power.
    @post Bought REX cannot be sold before 4 days counting from end of day of purchase.
    </details>

- [x] `.sellrex`

    <details>

    ```js
    {
        "price": 0.00010137714081746883,
        "rex": 1946385.7086999998, // amount of REX to be sold.
        "actions": 8
    }
    ```
    Sellrex action, sells REX in exchange for core tokens by converting REX stake back into core tokens at current exchange rate. If order cannot be processed, it gets queued until there is enough in REX pool to fill order, and will be processed within 30 days at most. If successful, user votes are updated, that is, proceeds are deducted from user's voting power. In case sell order is queued, storage change is billed to 'from' account.
    </details>

- [x] `.rentcpu` (DEPRECATED in favor of `powerup`)

    <details>
    ```js
    {
        "price": 14207.327700136308,
        "loan_payment": 0, // tokens paid for the loan
        "loan_fund": 0, // Loan balance represents a reserve that is used at expiration for automatic loan renewal.
        "actions": 0
    }
    ```
    Rentcpu action, uses payment to rent as many SYS tokens as possible as determined by market price and stake them for CPU for the benefit of receiver, after 30 days the rented core delegation of CPU will expire. At expiration, if balance is greater than or equal to `loan_payment`, `loan_payment` is taken out of loan balance and used to renew the loan. Otherwise, the loan is closed and user is refunded any remaining balance.
    </details>

- [x] `.rentnet` (DEPRECATED in favor of `powerup`)

    <details>

    ```js
    {
        "price": 14207.327700136308,
        "loan_payment": 0, // tokens paid for the loan
        "loan_fund": 0, // Loan balance represents a reserve that is used at expiration for automatic loan renewal.
        "actions": 0
    }
    ```
    Rentnet action, uses payment to rent as many SYS tokens as possible as determined by market price and stake them for NET for the benefit of receiver, after 30 days the rented core delegation of NET will expire. At expiration, if balance is greater than or equal to `loan_payment`, `loan_payment` is taken out of loan balance and used to renew the loan. Otherwise, the loan is closed and user is refunded any remaining balance.
    </details>

- [x] `.unstaketorex` (uncommon user action)

    <details>

    ```js
    {
        "from_net": 0, // amount of tokens to be unstaked from NET bandwidth and used for REX purchase,
        "from_cpu": 0, // amount of tokens to be unstaked from CPU bandwidth and used for REX purchase.
        "actions": 0
    }
    ```

    Unstaketorex action, uses staked core tokens to buy REX.

    @pre A voting requirement must be satisfied before action can be executed.
    @pre User must vote for at least 21 producers or delegate vote to proxy before buying REX.

    @post User votes are updated following this action.
    @post Tokens used in purchase are added to user's voting power.
    @post Bought REX cannot be sold before 4 days counting from end of day of purchase.
    </details>

- [x] `.mvtosavings` (uncommon user action)

    <details>

    ```js
    {
        "rex": 98641.5893, // amount of REX to be moved.
        "actions": 1
    }
    ```
    Mvtosavings action, moves a specified amount of REX into savings bucket. REX savings bucket never matures. In order for it to be sold, it has to be moved explicitly out of that bucket. Then the moved amount will have the regular maturity period of 4 days starting from the end of the day.
    </details>

- [x] `.mvfrsavings` (uncommon user action)

    <details>

    ```js
    {
        "rex": 0, // amount of REX to be moved.
        "actions": 0
    }
    ```
    Mvfrsavings action, moves a specified amount of REX out of savings bucket. The moved amount will have the regular REX maturity period of 4 days.
    </details>

## `.ram` (RAM as a resource)

### `.state`

- [x] `.rammarket`
    <details>

    ```js
    {
        "supply": 10000000000, // total RAMCORE supply
        "base": 275577060482, // 50/50 connector of RAM balance
        "quote": 5386227.986 // 50/50 connector of EOS balance
    }
    ```
    Uses Bancor math to create a 50/50 relay between two asset types.
    </details>

- [x] `.global`
    <details>

    ```js
    {
        "max_ram_size": 340685116416, // the amount of ram supply
        "total_ram_bytes_reserved": 65121421398, // total RAM bytes reserved
        "total_ram_stake": 43862146590 // total RAM reserved for smart contract utility
    }
    ```
    Uses Bancor math to create a 50/50 relay between two asset types.
    </details>

### `.actions`

- [x] `.buyram`
    <details>

    ```js
    {
        "price_kb": 49.95204603580562, // price in KB
        "quant": 9.0393, // the quantity of tokens to buy ram with.
        "actions": 10
    }
    ```
    Buy ram action, increases receiver's ram quota based upon current price and quantity of tokens provided.
    </details>

- [x] `.buyrambytes`
    <details>

    ```js
    {
        "price_kb": 0.0200192,
        "bytes": 424555, // the quantity of ram to buy specified in bytes.
        "actions": 288
    }
    ```
    Buy a specific amount of ram bytes action. Increases receiver's ram in quantity of bytes provided.
    </details>

### `.cpu` (CPU & NET as a resource)

### `.actions`

- [x] `.delegatebw` (DEPRECATED in favor of `powerup`)
    <details>

    ```js
    {
        "stake_net_quantity": 8.078099999999933, // tokens staked for NET bandwidth,
        "stake_cpu_quantity": 72.00140000000007, // tokens staked for CPU bandwidth,
        "actions": 321
    }
    ```
    Delegate bandwidth and/or cpu action. Stakes SYS from the balance of `from` for the benefit of `receiver`.

    @post All producers `from` account has voted for will have their votes updated immediately.
    </details>


- [x] `.undelegatebw` (DEPRECATED in favor of `powerup`)
    <details>

    ```js
    {
        "unstake_net_quantity": 1.05, // tokens to be unstaked from NET bandwidth
        "unstake_cpu_quantity": 11.3825, // tokens to be unstaked from CPU bandwidth
        "actions": 3
    }
    ```
    Undelegate bandwidth action, decreases the total tokens delegated by `from` to `receiver` and/or frees the memory associated with the delegation if there is nothing left to delegate.

    This will cause an immediate reduction in net/cpu bandwidth of the
    receiver.

    A transaction is scheduled to send the tokens back to `from` after the staking period has passed. If existing transaction is scheduled, it will be canceled and a new transaction issued that has the combined undelegated amount.

    The `from` account loses voting power as a result of this call and all producer tallies are updated.

    @post Unstaked tokens are transferred to `from` liquid balance via a deferred transaction with a delay of 3 days.
    @post If called during the delay period of a previous `undelegatebw` action, pending action is canceled and timer is reset.
    @post All producers `from` account has voted for will have their votes updated immediately.
    @post Bandwidth and storage for the deferred transaction are billed to `from`.
    </details>
