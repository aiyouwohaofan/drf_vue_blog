<template>

  <BlogHeader/>

  <div id="article-create">
    <h3>更新文章</h3>
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
        <input v-model="labels" type="text" placeholder="输入标签，用逗号分隔">
      </div>
      <div class="form-elem">
        <span>正文:</span>
        <textarea v-model="content" placeholder="输入正文" cols="80" rows="20"></textarea>
      </div>
      <div class="form-elem">
        <button v-on:click.prevent="submit">提交</button>
      </div>
      <div class="form-elem">
        <button v-on:click.prevent="deleteArticle" style="background-color: darkred">删除</button>
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
    name: "ArticleEdit",
    components: {BlogHeader, BlogFooter},
    data: function() {
      return {
        title: '',
        content: '',
        categories: [],
        selectedCategory: null,
        labels: '',
        articleID: null,
      }
    },
    mounted() {
      axios
          .get('/api/category')
          .then(response => this.categories = response.data);
      const that = this;
      axios
          .get('/api/article/' + that.$route.params.id + '/')
          .then(function(response) {
            const data = response.data;
            that.title = data.title;
            that.content = data.content;
            that.selectedCategory = data.category;
            that.labels = data.labels.join(',');
            that.articleID = data.id;
          })
    },
    methods: {
      categoryStyle(category) {
        if(this.selectedCategory !== null && category.id === this.selectedCategory.id) {
          return {
            background: 'black',
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
                let data = {
                  title: that.title,
                  content: that.content,
                };
                data.category_id = that.selectedCategory ? that.selectedCategory.id : null;
                data.labels = that.labels
                    .split(/[,，]/)
                    .map(x => x.trim())
                    .filter(x => x.charAt(0) !== '');
                const token = localStorage.getItem('access.myblog');
                axios
                    .put('/api/article/' + that.articleID + '/', data, {headers: {Authorization: 'Bearer ' + token}})
                    .then(function(response) {
                      that.$router.push({name: 'ArticleDetail', params: {id: response.data.id}});
                    })
              }
              else {
                alert('令牌过期，请重新登录。')
              }
            })
      },
      deleteArticle() {
        const that = this;
        const token = localStorage.getItem('access.myblog');
        authorization()
            .then(function(response) {
              if(response[0]) {
                axios
                    .delete('/api/article/' + that.articleID + '/', {headers: {Authorization: 'Bearer ' + token}})
                    .then(() => that.$router.push({name: 'Home'}))
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
    padding-right: 10px;
  }
  .form-elem {
    padding: 10px
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
    border-redius: 5px;
    width: 60px;
  }
</style>