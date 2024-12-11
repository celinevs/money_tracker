<template>
  <div>
    <h1>New Transaction Form</h1>
    <p> Transaction category: {{ category }}</p>
    <form @submit.prevent="submit"> <!-- Prevent default form submission -->
      <label for="date">Date:</label>
      <input type="date" v-model="dataentry.date" class="form-control" id="date" placeholder="Enter date" /> <br>

      <label for="name">Transaction name:</label>
      <input type="text" v-model="dataentry.name" class="form-control" id="name" placeholder="Enter transaction name" /> <br>

      <label for="amount">Amount:</label>
      <input type="number" v-model="dataentry.amount" class="form-control" id="amount" placeholder="Enter amount in Rupiah" /> <br>

      <label for="desc">Transaction description:</label>
      <input type="text" v-model="dataentry.desc" class="form-control" id="desc" placeholder="Enter transaction description" /> <br>

      <input type="submit" value="Submit" />
    </form>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data() {
    return {
      dataentry: {
        date: "",
        name: "",
        category: this.$route.params.category,  // Will be set via the route parameter
        amount: "",
        desc: "",
      },
    };
  },
  mounted() {
  console.log('Category on mount:', this.category);  // Check if the category is correctly retrieved
},
  computed: {
    category() {
      return this.$route.params.category || '';  // Access the category from the route params
    },
  },
  methods: {
    submit() {
      console.log('Category before submit:', this.dataentry.category);
      const path = "http://127.0.0.1:5000/form"; // Backend endpoint
      axios
      .post(path, {
          name: this.dataentry.name,
          date: this.dataentry.date, // Ensure proper format like YYYY-MM-DD
          category: this.dataentry.category,
          amount: parseFloat(this.dataentry.amount), // Ensure numeric value
          desc: this.dataentry.desc,
        })
        .then((response) => {
          console.log("Transaction Submitted Successfully:", response.data);
          alert("Transaction Submitted Successfully!");
          this.$router.push({ name: 'workspace' });;
        })
        .catch((error) => {
          console.error("Error Submitting Transaction:", error.response || error);
          alert("Failed to Submit Transaction. Please check your inputs.");
        });
    },
  },
};
</script>

