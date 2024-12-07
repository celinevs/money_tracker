<template>
    <div>
        <p>{{ msg }}</p>
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