package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
	"testing"
)

func getTestData() ObjectInfo {
	jsonFile, err := os.Open("test.json")
	if err != nil {
		fmt.Println(err)
	}
	defer jsonFile.Close()
	text, err := ioutil.ReadAll(jsonFile)
	if err != nil {
		fmt.Println(err)
	}
	var ob ObjectInfo
	err = json.Unmarshal([]byte(text), &ob)
	if err != nil {
		fmt.Println("error:", err)
	}
	return ob
}

func TestCalculateRevenue(t *testing.T) {
	transactions := getTestData().Transactions
	values := getValues(transactions)
	if values.Revenue != 30000 {
		t.Errorf("Calculating revenue is wrong")
	}
}

func TestCalculateExpenses(t *testing.T) {
	transactions := getTestData().Transactions
	values := getValues(transactions)
	if values.Expenses != 4500.50 {
		t.Errorf("Calculating expenses is wrong")
	}
}

func TestCalculateGrossProfit(t *testing.T) {
	transactions := getTestData().Transactions
	values := getValues(transactions)
	if values.Profit != 20000 {
		t.Errorf("Calculating gross profit is wrong")
	}
}

func TestCalculateAssetsIfOnlyCredit(t *testing.T) {
	transactions := getTestData().Transactions
	values := getValues(transactions)
	if values.Assets != -500 {
		t.Errorf("Calculating assets is wrong")
	}
}
