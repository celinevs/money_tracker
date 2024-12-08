<template>
    <div>
        <h1>New Transaction Form</h1>
        <form>
          <label for="date">Date:</label>
                <input type="date" class="form-control" id="date" v-model="transaction.date" placeholder="Enter date">
          <label for="amount">Amount:</label>
                <input type="number" class="form-control" id="amount" v-model="transaction.amount" placeholder="Enter amount in Rupiah">
          <label for="name">Transaction name:</label>
                <input type="text" class="form-control" id="name" v-model="transaction.name" placeholder="Enter transaction name">
          <label for="desc">Transaction description:</label>
                <input type="text" class="form-control" id="desc" v-model="transaction.desc" placeholder="Enter transaction description">
        </form>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    name: 'workspace',
    data() {
        return {
            msg: '' // This will store the response message
        };
    },
    methods: {
        async getResponse() {
            const path = 'http://127.0.0.1:5000/workspace';
      axios.get(path)
        .then((res) => {
          this.msg = res.data;
        })
        .catch((error) => {

          console.error(error);
        });
    },
  },
  created() {
    this.getResponse();
  },
};
</script>