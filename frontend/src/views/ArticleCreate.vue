<template>

  <BlogHeader/>

  <div id="article-create">
    <h3>发表文章</h3>
    <form id="image_form">
      <div class="form-elem">
        <span>图片:</span>
        <input v-on:change="onFileChange" type="file" id="file">
      </div>
    </form>
    <form>
      <div class="form-elem">
        <span>标题:</span>
        <input v-model="title" type="text" placeholder="输入标题">
      </div>
      <div class="form-elem">
        <span>分类:</span>
        <span v-for="category in categories" :key="category.id">
          <button class="category-btn" :style="categoryStyle(category)" @click.prevent="chooseCategory(category)">
            {{ category.title }}
          </button>
        </span>
      </div>
      <div class="form-elem">
        <span>标签:</span>
        <input v-model="labels" type="text" placeholder="请输入标签，用逗号分隔">
      </div>
      <div class="form-elem">
        <span>正文:</span>
        <textarea v-model="content" placeholder="请输入正文" cols="80" rows="20"></textarea>
      </div>
      <div class="form-elem">
        <button v-on:click.prevent="submit">提交</button>
      </div>
    </form>
  </div>

  <BlogFooter/>

</template>

<script>
  import BlogHeader from '@/components/BlogHeader.vue';
  import BlogFooter from '@/components/BlogFooter.vue';
  import axios from 'axios';
  import authorization from '@/utils/authorization';

  export default {
    name: "ArticleCreate",
    components: {BlogHeader, BlogFooter},
    data: function() {
      return {
        title: '',
        content: '',
        categories: [],
        selectedCategory: null,
        labels: '',
        avatarID: null,
      }
    },
    mounted() {
      axios
          .get('/api/category/')
          .then(response => this.categories = response.data)
    },
    methods: {
      onFileChange(e) {
        const file = e.target.files[0];
        let formData = new FormData();
        formData.append('content', file);
        axios
            .post('/api/avatar/', formData, {headers: {
              'Content-Type': 'multipart/form-data',
              'Authorization': 'Bearer ' + localStorage.getItem('access.myblog')
            }})
            .then(response => this.avatarID = response.data.id)
      },
      categoryStyle(category) {
        if(this.selectedCategory !== null && category.id === this.selectedCategory.id) {
          return {
            backgroundColor: 'black',
          }
        }
        return {
          backgroundColor: 'lightgrey',
          color: 'black',
        }
      },
      chooseCategory(category) {
        if(this.selectedCategory !== null && this.selectedCategory.id === category.id) {
          this.selectedCategory = null
        }
        else {
          this.selectedCategory = category;
        }
      },
      submit() {
        const that = this;
        authorization()
            .then(function(response) {
              if(response[0]) {
                let data = {title: that.title, content: that.content};
                data.avatar_id = that.avatarID;
                if(that.selectedCategory) {
                  data.category_id = that.selectedCategory.id
                }
                data.labels = that.labels
                    .split(/[,，]/)
                    .map(x => x.trim())
                    .filter(x => x.charAt(0) !== '');
                const token = localStorage.getItem('access.myblog');
                axios
                    .post('/api/article/', data, {headers: {Authorization: 'Bearer ' + token}})
                    .then(function(response) {
                      that.$router.push({name: 'ArticleDetail', params: {id: response.data.id}});
                    })
              }
              else {
                alert('令牌过期，请重新登录。')
              }
            })
      }
    }
  }
</script>

<style scoped>
  .category-btn {
    margin-right: 10px;
  }
  #article-create {
    text-align: center;
    font-size: large;
  }
  form {
    text-align: left;
    padding-left: 100px;
    padding-right: 100px;
  }
  .form-elem {
    padding: 10px;
  }
  input {
    height: 25px;
    padding-left: 10px;
    width: 50%;
  }
  button {
    height: 35px;
    cursor: pointer;
    border: none;
    outline: none;
    background: steelblue;
    color: whitesmoke;
    border-radius: 5px;
    width: 60px;
  }
</style>