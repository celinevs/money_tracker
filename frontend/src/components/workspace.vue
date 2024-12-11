<template>
  <div>
    <div class="header">
      <h1>Transaction Board</h1>
      <button @click="logout">Logout</button>
    </div>
    <div class="controls">
      <p><b>Start Date:</b> <input type="date"></p>
      <p><b>End Date:</b> <input type="date"></p>
      <p><b>Total Budget:</b> <span>{{ totalBudget }}</span></p>
    </div>
    <div class="board">
      <div 
        v-for="(transactions, category) in groupedTransactions" 
        :key="category" 
        class="column"
        :class="{ overBudget: calculateTotal(category) > budgetLimit }"
      >
        <div class="column-header">
          <h2>{{ category }}</h2>
          <button @click="addTransaction(category)">+</button>
        </div>
        <div 
          v-for="(transaction, index) in transactions" 
          :key="index" 
          class="transaction"
          @click="viewTransaction(transaction)"
        >
          {{ transaction.name }}
        </div>
        <p class="total">Total: {{ calculateTotal(category) }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'TransactionBoard',
  data() {
    return {
      groupedTransactions: {},
      budgetLimit: 500000, // Example budget limit for each category
      totalBudget: 0,
    };
  },
  mounted() {
    this.fetchTransactions();
  },
  methods: {
    async fetchTransactions() {
      try {
        const res = await axios.get('http://127.0.0.1:5000/workspace');
        this.groupedTransactions = res.data;
        this.calculateTotalBudget();
      } catch (error) {
        console.error('Error fetching transactions:', error);
      }
    },
    viewTransaction(transaction) {
      alert(`Transaction Details:\nName: ${transaction.name}\nAmount: ${transaction.amount}\nDescription: ${transaction.description}\nDate: ${transaction.date}`);
    },
    addTransaction(category) {
      this.$router.push({ name: 'form' ,params: { category }});
    },
    logout() {
      alert('Logout clicked');
    },
    calculateTotal(category) {
      const transactions = this.groupedTransactions[category] || [];
      return transactions.reduce((sum, transaction) => sum + transaction.amount, 0);
    },
    calculateTotalBudget() {
      this.totalBudget = Object.keys(this.groupedTransactions).reduce((total, category) => {
        return total + this.calculateTotal(category);
      }, 0);
    },
  },
};
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.controls {
  margin-bottom: 20px;
}

.board {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.column {
  border: 1px solid #ccc;
  border-radius: 5px;
  width: 200px;
  padding: 10px;
  background-color: #f9f9f9;
}

.column-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.transaction {
  background: #fff;
  padding: 5px;
  margin: 5px 0;
  border: 1px solid #ddd;
  cursor: pointer;
  transition: background 0.3s;
}

.transaction:hover {
  background: #f0f0f0;
}

.total {
  margin-top: 10px;
  font-weight: bold;
}

.overBudget {
  background-color: #fdd;
}
</style>
