<template>
  <div>
    <div class="header">
      <h1>Transaction Board</h1>
      <button @click="logout">Logout</button>
    </div>
    <div class="controls">
      <p><b>Total Budget:</b> <span>{{ totalBudget }}</span></p>
    </div>
    <div class="filters">
      <h3>Filter Categories</h3>
      <div class="filter-row">
        <p><b>Start Date:</b> <input type="date" v-model="startDate"></p>
        <p><b>End Date:</b> <input type="date" v-model="endDate"></p>
      </div>
      <div v-for="(transactions, category) in groupedTransactions" :key="category" class="filter-item">
        <label>
          <input 
            type="checkbox" 
            v-model="selectedCategories" 
            :value="category"
          />
          {{ category }}
        </label>
      </div>
      <button @click="applyFilters" class="apply-button">Apply Filters</button>
    </div>
    <div class="board">
      <div 
        v-for="(transactions, category) in filteredTransactions" 
        :key="category" 
        class="column"
        :class="{ overBudget: calculateTotal(category) > budgetLimit }"
      >
        <div class="column-header">
          <h2>{{ category }}</h2>
          <button @click="addTransaction(category)" class="add-button">+</button>
        </div>
        <div 
          v-for="(transaction, index) in transactions" 
          :key="index" 
          class="transaction-card"
          @click="editTransaction(transaction)"
        >
          <div class="transaction-card-header">
            <h4>{{ transaction.amount }} IDR</h4>
            <p>{{ transaction.date }}</p>
          </div>
          <p>{{ transaction.description }}</p>
        </div>
        <p class="total">Total: {{ calculateTotal(category) }}</p>
      </div>
    </div>

    <!-- Edit Form Modal -->
    <div v-if="showEditForm" class="modal-overlay" @click="closeEditForm">
      <div class="modal-content" @click.stop>
        <h3>Edit Transaction</h3>
        <form @submit.prevent="saveTransaction">
          <label for="name">Name</label>
          <input v-model="selectedTransaction.name" id="name" type="text" required />
          
          <label for="amount">Amount</label>
          <input v-model="selectedTransaction.amount" id="amount" type="number" required />
          
          <label for="description">Description</label>
          <textarea v-model="selectedTransaction.description" id="description" required></textarea>

          <label for="date">Date</label>
          <input v-model="selectedTransaction.date" id="date" type="date" required />

          <div class="modal-actions">
            <button type="submit" class="save-button">Save</button>
            <button type="button" @click="deleteTransaction(selectedTransaction)" class="cancel-button">Delete</button>
          </div>
        </form>
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
      selectedCategories: [],
      filteredTransactions: {},
      startDate: '',
      endDate: '',
      showEditForm: false,
      selectedTransaction: {},
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
        this.filteredTransactions = this.groupedTransactions;
        this.calculateTotalBudget();
      } catch (error) {
        console.error('Error fetching transactions:', error);
      }
    },
    editTransaction(transaction) {
      this.selectedTransaction = { ...transaction }; // Clone the transaction to avoid direct mutation
      this.showEditForm = true;
    },
    saveTransaction() {
      // Update the transaction in the database
      axios.put(`http://127.0.0.1:5000/workspace/${this.selectedTransaction.id}`, this.selectedTransaction)
        .then(response => {
          this.fetchTransactions(); // Refresh data
          this.closeEditForm();
        })
        .catch(error => {
          console.error('Error updating transaction:', error);
        });
    },
    deleteTransaction(transaction) {
      // Delete the transaction from the database
      axios.delete(`http://127.0.0.1:5000/workspace/${transaction.id}`)
        .then(response => {
          this.fetchTransactions(); // Refresh data
        })
        .catch(error => {
          console.error('Error deleting transaction:', error);
        });
    },
    addTransaction(category) {
      this.$router.push({ name: 'form', params: { category } });
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
    applyFilters() {
      const filteredByCategory = this.selectedCategories.length === 0
        ? this.groupedTransactions
        : Object.keys(this.groupedTransactions)
            .filter(category => this.selectedCategories.includes(category))
            .reduce((filtered, category) => {
              filtered[category] = this.groupedTransactions[category];
              return filtered;
            }, {});

      this.filteredTransactions = Object.keys(filteredByCategory).reduce((filtered, category) => {
        const transactions = filteredByCategory[category].filter(transaction => {
          const transactionDate = new Date(transaction.date);
          const start = this.startDate ? new Date(this.startDate) : null;
          const end = this.endDate ? new Date(this.endDate) : null;
          return (!start || transactionDate >= start) && (!end || transactionDate <= end);
        });
        if (transactions.length > 0) {
          filtered[category] = transactions;
        }
        return filtered;
      }, {});
    },
    closeEditForm() {
      this.showEditForm = false;
      this.selectedTransaction = {};
    },
  },
};
</script>

<style scoped>
/* General Layout */
body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f7f7f7;
  margin: 0;
  padding: 0;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #007bff;
  color: white;
  padding: 20px;
  border-radius: 5px 5px 0 0;
}

h1 {
  margin: 0;
  font-size: 28px;
}

button {
  padding: 8px 16px;
  border: none;
  background-color: #007bff;
  color: white;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #0056b3;
}

.controls, .filters {
  padding: 20px;
  background-color: white;
  border-radius: 5px;
  margin-bottom: 20px;
}

.filters h3 {
  font-size: 20px;
}

.filter-row {
  display: flex;
  gap: 15px;
}

.filter-item {
  margin: 10px 0;
}

.apply-button {
  background-color: #28a745;
  padding: 10px 20px;
  font-size: 16px;
}

.apply-button:hover {
  background-color: #218838;
}

/* Board Layout */
.board {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.column {
  border-radius: 8px;
  padding: 15px;
  background-color: #ffffff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  width: 220px;
  margin-bottom: 20px;
  transition: box-shadow 0.3s ease;
}

.column:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.column-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.column-header h2 {
  font-size: 20px;
  margin: 0;
}

.add-button {
  background-color: #f39c12;
  border-radius: 50%;
  width: 35px;
  height: 35px;
  font-size: 20px;
  padding: 0;
  color: white;
  text-align: center;
  line-height: 35px;
  cursor: pointer;
}

.add-button:hover {
  background-color: #e67e22;
}

.transaction-card {
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  margin: 15px 0;
  padding: 15px;
  cursor: pointer;
  transition: transform 0.3s ease, background-color 0.3s ease;
}

.transaction-card:hover {
  background: #f9f9f9;
  transform: scale(1.05);
}

.transaction-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.transaction-card-header h4 {
  margin: 0;
  font-size: 18px;
  color: #e74c3c;
}

.transaction-card-header p {
  margin: 0;
  font-size: 12px;
  color: #888;
}

.total {
  font-weight: bold;
  margin-top: 20px;
}

.overBudget {
  background-color: #f8d7da;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: #fff;
  padding: 25px;
  border-radius: 8px;
  width: 400px;
  max-width: 100%;
}

input, textarea {
  width: 100%;
  padding: 12px;
  margin: 8px 0;
  border: 1px solid #ddd;
  border-radius: 5px;
}

textarea {
  resize: vertical;
  min-height: 80px;
}

.modal-actions {
  display: flex;
  justify-content: space-between;
}

.save-button {
  background-color: #28a745;
  width: 48%;
}

.save-button:hover {
  background-color: #218838;
}

.cancel-button {
  background-color: #dc3545;
  width: 48%;
}

.cancel-button:hover {
  background-color: #c82333;
}
</style>
