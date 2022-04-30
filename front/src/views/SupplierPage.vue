<template>
    <table class="table table-bordered">
  <thead>
    <tr>
      <th>Supplier</th>
    </tr>
  </thead>
  <tbody>
    <tr v-for="agency in agencies" :key="agency.id" >
      <td class="text-left">{{ agency }}</td>
    </tr>
  </tbody>
</table>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRoute } from "vue-router";
import axios from 'axios';

export default {

    setup() {
        const route = useRoute();
        const agencies = ref(null);

        async function getList() {
            await axios
            .get('http://127.0.0.1:5000/agencies',{ 
                params: route.query
            })
            .then(function (res) {
                agencies.value = res.data;
            })
            .catch(function (error) {
                if (error.response.status == 401) {
                    console.log('Error!');
                }
            });
        }

        onMounted(() => {
            getList();
        });

        return { agencies }
    }
}
</script>