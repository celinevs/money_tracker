<template>
  <div>
    <div class="header">
      <h1>Transaction Board</h1>
      <button @click="logout">Logout</button>
    </div>
    <div class="controls">
      <p><b>Total Spent:</b> <span>{{ totalBudget }}</span></p>
      <p><b>Budget limit:</b> <span>{{ budgetLimit }}</span></p>
    </div>
    <div class="filters">
      <h3>Filter Categories</h3>
      <div class="filter-row">
        <p><b>Start Date:</b> <input type="date" v-model="startDate"></p>
        <p><b>End Date:</b> <input type="date" v-model="endDate"></p>
      </div>
      <div class="filter-categories">
        <label v-for="category in ['A', 'B', 'C', 'D', 'E']" :key="category">
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
          <button @click="openAddForm(category)" class="add-button">+</button>
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

    <!-- Add Form Modal -->
    <div v-if="showAddForm" class="modal-overlay" @click="closeAddForm">
      <div class="modal-content" @click.stop>
        <h3>Add Transaction</h3>
        <form @submit.prevent="saveNewTransaction">
          <label for="newName">Name</label>
          <input v-model="newTransaction.name" id="newName" type="text" required />
          
          <label for="newAmount">Amount</label>
          <input v-model="newTransaction.amount" id="newAmount" type="number" required />
          
          <label for="newDescription">Description</label>
          <textarea v-model="newTransaction.description" id="newDescription" required></textarea>

          <label for="newDate">Date</label>
          <input v-model="newTransaction.date" id="newDate" type="date" required />

          <div class="modal-actions">
            <button type="submit" class="save-button">Add</button>
            <button type="button" @click="closeAddForm" class="cancel-button">Cancel</button>
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
      showAddForm: false,
      selectedTransaction: {},
      newTransaction: {
        name: '',
        amount: '',
        description: '',
        date: '',
        category: '',
      },
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
      axios.put(`http://127.0.0.1:5000/workspace/${this.selectedTransaction.id}`, this.selectedTransaction)
        .then(() => {
          this.fetchTransactions(); // Refresh data
          this.closeEditForm();
        })
        .catch(error => {
          console.error('Error updating transaction:', error);
        });
    },
    deleteTransaction(transaction) {
      axios.delete(`http://127.0.0.1:5000/workspace/${transaction.id}`)
        .then(() => {
          this.fetchTransactions(); // Refresh data
        })
        .catch(error => {
          console.error('Error deleting transaction:', error);
        });
    },
    openAddForm(category) {
      this.newTransaction = { name: '', amount: '', description: '', date: '', category };
      this.showAddForm = true;
    },
    logout() {
      this.$router.push({ name: 'login'});
    },
    saveNewTransaction() {
      axios.post('http://127.0.0.1:5000/form', this.newTransaction)
        .then(() => {
          this.fetchTransactions(); // Refresh data
          this.closeAddForm();
        })
        .catch(error => {
          console.error('Error adding transaction:', error);
        });
    },
    closeEditForm() {
      this.showEditForm = false;
      this.selectedTransaction = {};
    },
    closeAddForm() {
      this.showAddForm = false;
      this.newTransaction = {};
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
  const allCategories = ['a', 'b', 'c', 'd', 'e']; // Fixed categories list

  // Start by including all selected categories, even if empty
  const filteredByCategory = this.selectedCategories.reduce((filtered, category) => {
    filtered[category] = this.groupedTransactions[category] || []; // Include even if empty
    return filtered;
  }, {});

  // Apply date filters if startDate or endDate are provided
  this.filteredTransactions = Object.keys(filteredByCategory).reduce((filtered, category) => {
    const transactions = (filteredByCategory[category] || []).filter(transaction => {
      const transactionDate = new Date(transaction.date);
      const start = this.startDate ? new Date(this.startDate) : null;
      const end = this.endDate ? new Date(this.endDate) : null;
      return (!start || transactionDate >= start) && (!end || transactionDate <= end);
    });

    // Ensure the category is included, even if no transactions match the date filter
    filtered[category] = transactions;
    return filtered;
  }, {});

  // Log for debugging
  console.log('Filtered Transactions:', this.filteredTransactions);
},

  },
};
</script>

<style scoped>
/* General Layout */
body {
  font-family: 'Poppins', Arial, sans-serif;
  background-color: #fffbf0;
  margin: 0;
  padding: 0;
  color: #333;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #ff7eb9;
  color: white;
  padding: 20px;
  border-radius: 15px 15px 0 0;
  box-shadow: 0 5px 10px rgba(0, 0, 0, 0.2);
}

h1 {
  margin: 0;
  font-size: 32px;
}

button {
  padding: 10px 18px;
  border: none;
  background-color: #ffb677;
  color: white;
  border-radius: 25px;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
  transition: transform 0.2s ease, background-color 0.3s ease;
}

button:hover {
  background-color: #ff6363;
  transform: translateY(-3px);
}

.controls, .filters {
  padding: 20px;
  background-color: #ffffff;
  border-radius: 15px;
  margin-bottom: 20px;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
}

.filters h3 {
  font-size: 22px;
  color: #ff7eb9;
}

.filter-row {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.filter-item {
  margin: 10px 0;
}

.filter-categories {
  display: flex;
  gap: 15px; /* Menambahkan jarak antar checkbox dan label */
  font-size: 16px;
}

.filter-categories label {
  display: flex;
  align-items: center;
}

.filter-categories input {
  margin-right: 8px; /* Memberikan jarak antara checkbox dan label */
}
.apply-button {
  background-color: #6cdbeb;
  padding: 12px 24px;
  font-size: 18px;
  border-radius: 20px;
}

.apply-button:hover {
  background-color: #38a3a5;
}

/* Board Layout */
.board {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 20px;
  padding: 20px;
}

.column {
  border-radius: 12px;
  padding: 20px;
  background-color: #ffeedb;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.column:hover {
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
  transform: translateY(-5px);
}

.column-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.column-header h2 {
  font-size: 22px;
  margin: 0;
  color: #ff7eb9;
}

.add-button {
  background-color: #ffd97d;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  font-size: 24px;
  padding: 0;
  color: white;
  text-align: center;
  line-height: 40px;
  cursor: pointer;
}

.add-button:hover {
  background-color: #f9a826;
}

.transaction-card {
  background: #ffffff;
  border: 2px solid #ffd97d;
  border-radius: 12px;
  margin: 15px 0;
  padding: 15px;
  cursor: pointer;
  transition: transform 0.3s ease, background-color 0.3s ease;
}

.transaction-card:hover {
  background: #fff3e0;
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
  color: #ff6363;
}

.transaction-card-header p {
  margin: 0;
  font-size: 12px;
  color: #999;
}

.total {
  font-weight: bold;
  margin-top: 20px;
  color: #ff7eb9;
}

.overBudget {
  background-color: #ffe6e6;
}



.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: #fffbf0; /* Match workspace background */
  padding: 25px;
  border-radius: 15px;
  width: 420px;
  max-width: 100%;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  color: #333; /* Text color matching the workspace */
}

.modal-content h3 {
  font-size: 24px;
  color: #ff7eb9; /* Match primary accent color */
  margin-bottom: 15px;
}

.modal-content label {
  font-weight: bold;
  margin-bottom: 5px;
  display: block;
}

input, textarea {
  width: 90%;
  padding: 12px;
  margin: 10px 0;
  border: 2px solid #ffd97d; /* Match transaction card borders */
  border-radius: 12px; /* Rounded corners consistent with cards */
  background: #ffffff;
  font-size: 16px;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

input:focus, textarea:focus {
  outline: none;
  border-color: #ff7eb9; /* Highlight matching primary color */
  box-shadow: 0 0 5px #ff7eb9;
}

textarea {
  resize: vertical;
  min-height: 80px;
}

.modal-actions {
  display: flex;
  justify-content: space-between;
  gap: 10px;
}

.save-button {
  background-color: #6cdbeb; /* Match "Apply Filters" button color */
  width: 48%;
  color: #fff;
  font-weight: bold;
  border-radius: 20px; /* Rounded consistent with workspace */
  padding: 12px;
  font-size: 16px;
  transition: transform 0.2s ease, background-color 0.3s ease;
}

.save-button:hover {
  background-color: #38a3a5;
  transform: translateY(-3px);
}

.cancel-button {
  background-color: #ff6363; /* Match "Cancel" button style */
  width: 48%;
  color: white;
  font-weight: bold;
  border-radius: 20px;
  padding: 12px;
  font-size: 16px;
  transition: transform 0.2s ease, background-color 0.3s ease;
}

.cancel-button:hover {
  background-color: #e63946;
  transform: translateY(-3px);
}

button {
  cursor: pointer;
}



</style>