package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"math"
	"os"
)

type ObjectInfo struct {
	Category       string        `json:"object_category"`
	ConnectionId   string        `json:"connection_id"`
	User           string        `json:"user"`
	CreationDate   string        `json:"object_creation_date"`
	Transactions   []Transaction `json:"data"`
	Currency       string        `json:"currency"`
	OriginType     string        `json:"object_origin_type"`
	OriginCategory string        `json:"object_origin_category"`
	Type           string        `json:"object_type"`
	Class          string        `json:"object_class"`
	BalanceDate    string        `json:"balance_date"`
}

type Transaction struct {
	AccountCode       string  `json:"account_code"`
	AccountCurrency   string  `json:"account_currency"`
	AccountIdentifier string  `json:"account_identifier"`
	AccountStatus     string  `json:"account_status"`
	AccountType       string  `json:"account_type"`
	AccountTypeBank   string  `json:"account_type_bank"`
	ValueType         string  `json:"value_type"`
	AccountCategory   string  `json:"account_category"`
	AccountName       string  `json:"account_name"`
	SystemAccount     string  `json:"system_account"`
	TotalValue        float64 `json:"total_value"`
}

type Metrics struct {
	GrossProfitMargin   float64
	NetProfitMargin     float64
	WorkingCapitalRatio float64
}

type Values struct {
	Revenue   float64
	Expenses  float64
	Profit    float64
	Assets    float64
	Liability float64
}

func stringInSlice(a string, list []string) bool {
	for _, b := range list {
		if b == a {
			return true
		}
	}
	return false
}

func getValues(transactions []Transaction) Values {
	// Returns revenue, expenses, profit, assets and liability.
	var values Values
	typesAssets := []string{"current", "bank", "current_accounts_receivable"}
	typesLiabilities := []string{"current", "current_accounts_payable"}

	for _, tr := range transactions {
		value := tr.TotalValue
		valueType := tr.ValueType
		category := tr.AccountCategory
		acType := tr.AccountType

		if category == "revenue" { // Total revenue
			values.Revenue += value
		} else if category == "expense" { // Total expenses
			values.Expenses += value
		} else if category == "assets" && valueType == "debit" && stringInSlice(acType, typesAssets) { // Total assets
			values.Assets += value
		} else if category == "assets" && valueType == "credit" && stringInSlice(acType, typesAssets) {
			values.Assets -= value
		} else if category == "liability" && valueType == "credit" && stringInSlice(acType, typesLiabilities) { // Total liability
			values.Liability += value
		} else if category == "liability" && valueType == "dedit" && stringInSlice(acType, typesLiabilities) {
			values.Liability -= value
		}

		// Gross profit
		if acType == "sales" && valueType == "debit" {
			values.Profit += value
		}
	}
	return values

}

func calculateMetrics(values Values) Metrics {
	// Calculates profit and working capital ratio
	var metrics Metrics
	if values.Revenue == 0 {
		metrics.GrossProfitMargin, metrics.NetProfitMargin = 0, 0
	} else {
		metrics.GrossProfitMargin = math.Round(values.Profit / values.Revenue * 100)
		metrics.NetProfitMargin = math.Round((values.Revenue - values.Expenses) / values.Revenue * 100)
	}

	if values.Liability == 0 {
		metrics.WorkingCapitalRatio = 0
	} else {
		metrics.WorkingCapitalRatio = math.Round(values.Assets / values.Liability * 100)
	}
	return metrics
}

func main() {
	// Open file
	jsonFile, err := os.Open("data.json")
	if err != nil {
		fmt.Println(err)
	}
	defer jsonFile.Close()

	// Read file
	text, err := ioutil.ReadAll(jsonFile)
	if err != nil {
		fmt.Println(err)
	}

	var ob ObjectInfo
	err = json.Unmarshal([]byte(text), &ob)
	if err != nil {
		fmt.Println("error:", err)
	}

	values := getValues(ob.Transactions)
	metrics := calculateMetrics(values)

	fmt.Printf("Revenue: $%.2f\n", values.Revenue)
	fmt.Printf("Expenses: $%.2f\n", values.Expenses)
	fmt.Printf("Profit: $%.2f\n", values.Profit)
	fmt.Printf("Gross Profit Margin: %.0f%%\n", metrics.GrossProfitMargin)
	fmt.Printf("Net Profit Margin: %.0f%%\n", metrics.NetProfitMargin)
	fmt.Printf("Working Capital Ratio: %.0f%%\n", metrics.WorkingCapitalRatio)
}
