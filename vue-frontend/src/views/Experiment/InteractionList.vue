<template>
  <div class="main">
    <el-page-header @back="goBack" content="测试列表">
    </el-page-header>
    <div class="content">
      <h3 style="letter-spacing: 1px; font-weight: 400; padding-bottom: 20px; text-align: center">
        {{ this.thisExperiment.name }}的交互记录
      </h3>
    </div>
    <template v-if="interactionList && interactionList.length">
      <div class="table-container">
        <el-input v-model="filterKey" placeholder="请搜索问题" size="large" clearable @input="updateFilter"
          style="width: 300px;margin-left:0px; margin-bottom: 20px;">
        </el-input>

        <!-- 基础能力测试交互记录列表 -->
        <el-table v-if="thisExperiment.type === 1" :data="pageList" style="width: 100%" stripe v-loading="loading"
          border>
          <!-- <el-table-column label="QA ID" prop="QAid"></el-table-column> -->
          <el-table-column label="详情" type="expand" width="150px">
            <template slot-scope="scope">
              <div>
                <el-form label-position="left" inline class="demo-table-expand">
                  <el-form-item label="时间:">
                    <span>{{ scope.row.time }}</span>
                  </el-form-item>
                  <el-form-item label="关键字:">
                    <div v-if="scope.row.keyword.length">
                      <span v-for="(item, index) in scope.row.keyword" :key="index">
                        {{ item }}
                      </span>
                    </div>
                    <el-tag type="info" v-else>无</el-tag>
                  </el-form-item>
                  <el-form-item label="规则化得分:">
                    <span v-if="scope.row.keywords_score.length">{{ scope.row.keywords_score[0] }}</span>
                    <el-tag type="info" v-else>无</el-tag>
                  </el-form-item>
                  <el-form-item label="黑名单得分:">
                    <span v-if="scope.row.blacklist_score.length">{{ scope.row.blacklist_score[0] }}</span>
                    <el-tag type="info" v-else>无</el-tag>
                  </el-form-item>
                  <el-form-item label="大模型得分:">
                    <span v-if="scope.row.llm_score.length">{{ scope.row.llm_score[0] }}</span>
                    <el-tag type="info" v-else>无</el-tag>
                  </el-form-item>
                  <el-form-item label="最终得分:">
                    <span v-if="scope.row.fin_score">{{ scope.row.fin_score }}</span>
                    <el-tag type="warning" v-else>暂无</el-tag>
                  </el-form-item>
                </el-form>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="问题">
            <template slot-scope="scope">
              <div style="height: 70px; overflow: auto; display: flex;justify-content: flex-start;">{{ scope.row.Q }}
              </div>
            </template>
          </el-table-column>
          <el-table-column label="回答">
            <template slot-scope="scope">
              <div style="height: 70px; overflow: auto; display: flex;justify-content: flex-start;">{{ scope.row.A }}
              </div>
            </template>
          </el-table-column>
          <el-table-column label="领域" prop="field" width="200px" align="center">
          </el-table-column>
        </el-table>

        <!-- 幻觉测试交互记录列表 -->
        <el-table v-else-if="thisExperiment.type === 2" :data="pageList" style="width: 100%" stripe v-loading="loading"
          border>
          <el-table-column label="时间" prop="time" width="200%">
          </el-table-column>
          <el-table-column label="问题">
            <template slot-scope="scope">
              <div style="height: 70px; overflow: auto; display: flex;justify-content: flex-start;">{{ scope.row.Q }}
              </div>
            </template>
          </el-table-column>
          <el-table-column label="回答" type="expand" width="50%">
            <template slot-scope="scope">
              <!-- <div style="height: 70px; overflow: auto; display: flex;justify-content: flex-start;">{{ scope.row.A }}</div> -->
              <el-form label-position="left" class="three-times-answer">
                <el-form-item>
                  <h4>第一次回答</h4>
                  <span>{{ scope.row.A[0] }}</span>
                </el-form-item>
                <el-form-item>
                  <h4>第二次回答</h4>
                  <span>{{ scope.row.A[1] }}</span>
                </el-form-item>
                <el-form-item>
                  <h4>第三次回答</h4>
                  <span>{{ scope.row.A[2] }}</span>
                </el-form-item>
                <!-- <el-form-item>
                  <h4>评估模型prompt</h4>
                  <span>{{ scope.row.prompt }}</span>
                </el-form-item> -->
              </el-form>
            </template>
          </el-table-column>
          <el-table-column label="领域" prop="field" width="200px" align="center">
          </el-table-column>
          <!-- <el-table-column label="LLMEval得分" prop="llm_score" width="120%" align="center">
            <template slot-scope="scope">
              <span v-if="scope.row.llm_score.length">{{ scope.row.llm_score }}</span>
              <el-tag type="info" v-else>无</el-tag>
            </template>
          </el-table-column> -->
          <el-table-column label="幻觉最终判断" prop="fin_score" width="120%" align="center">
            <template slot-scope="scope">
              <el-tag effect="light" v-if="scope.row.fin_score === '1.0'" type="success">无幻觉</el-tag>
              <el-tag effect="light" v-else-if="scope.row.fin_score === '0.0'" type="danger">有幻觉</el-tag>
              <el-tag effect="light" v-else type="info">缺失</el-tag>
            </template>
          </el-table-column>
        </el-table>

        <!-- 毒性测试的交互记录表 -->
        <el-table v-else-if="thisExperiment.type === 3" :data="pageList" style="width: 100%" stripe v-loading="loading"
          border>
          <el-table-column label="时间" prop="time" width="200%">
          </el-table-column>
          <el-table-column label="问题">
            <template slot-scope="scope">
              <div style="height: 70px; overflow: auto; display: flex;justify-content: flex-start;">{{ scope.row.Q }}
              </div>
            </template>
          </el-table-column>
          <el-table-column label="回答" type="expand" width="50%">
            <template slot-scope="scope">
              <!-- <div style="height: 70px; overflow: auto; display: flex;justify-content: flex-start;">{{ scope.row.A }}</div> -->
              <el-form label-position="left" class="three-times-answer">
                <el-form-item>
                  <h4>回答</h4>
                  <span>{{ scope.row.A}}</span>
                </el-form-item>
              </el-form>
            </template>
          </el-table-column>
          <el-table-column label="领域" prop="field" width="200px" align="center">
          </el-table-column>
          <el-table-column label="毒性最终判断" prop="fin_score" width="120%" align="center">
            <template slot-scope="scope">
              <el-tag effect="light" v-if="scope.row.fin_score === '1.0'" type="success">无毒性</el-tag>
              <el-tag effect="light" v-else-if="scope.row.fin_score === '0.0'" type="danger">有毒性</el-tag>
              <el-tag effect="light" v-else type="info">缺失</el-tag>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <div class="pagination-container" style="margin-top: 20px;">
        <el-pagination background @size-change="handleSizeChange" @current-change="handleCurrentChange"
          :current-page="currentPage" :page-sizes="[5, 10, 20, 30, 50]" :page-size="pageSize" :total="filteredTotal"
          layout="total, sizes, prev, pager, next, jumper">
        </el-pagination>
      </div>
    </template>
    <div v-else>
      <el-empty description="暂无交互记录"></el-empty>
    </div>
  </div>
</template>

<script>
import { getInteraction } from "@/api/expOperation"

export default {
  name: "interactionList",
  data() {
    return {
      filterKey: '',
      thisExperiment: {},
      interactionList: [],
      currentPage: 1,
      pageSize: 10,
      pageList: [], // 用于显示当前页的数据
      loading: true,
      filteredTotal: 0
    }
  },
  mounted() {
    let storedExperiment = localStorage.getItem('thisExperiment');
    if (storedExperiment) {
      this.thisExperiment = JSON.parse(storedExperiment);
    }
    else {
      // 处理没有数据的情况，可能是跳转到此页面或刷新页面
      this.$router.push("/projectsList")
    }
    this.load()
    setTimeout(() => {
      this.loading = false
    }, 500);

  },
  methods: {
    load() {
      getInteraction(this.thisExperiment.id, this.thisExperiment.type).then(res => {
        if (res.success)
          this.interactionList = res.data
        console.log("交互记录", this.interactionList)
        this.updatePageList()
        this.updateTotalPages(this.interactionList)
      })
    },
    goBack() {
      this.$router.go(-1); // 返回上一个页面
    },
    updateTotalPages(filteredData) {
      const totalItems = filteredData.length;
      this.filteredTotal = totalItems; // 更新过滤后的总项数
      this.totalPages = Math.ceil(totalItems / this.pageSize);
    },
    updateFilter() {
      const filteredData = this.interactionList.filter(item => {
        return item.Q.toLowerCase().includes(this.filterKey.toLowerCase())
      });
      this.updateTotalPages(filteredData);  // 更新总页数
      this.updatePageList(filteredData);
    },
    // 用于处理当前页变化
    handleSizeChange(newSize) {
      this.pageSize = newSize;
      this.updateFilter();
    },
    // 更新当前页的 QA 列表
    updatePageList(filteredData = this.interactionList) {
      const startIndex = (this.currentPage - 1) * this.pageSize;
      const endIndex = startIndex + this.pageSize;
      this.pageList = (filteredData || []).slice(startIndex, endIndex);  // 确保总是有数组可操作
    },
    handleCurrentChange(newPage) {
      this.currentPage = newPage;
      this.updateFilter();
    },

  }
}
</script>

<style scoped>
.table-container {
  max-width: 2000px;
  /* 设置你希望的最大宽度 */
  margin: auto;
  /* 这将使得表格居中 */
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  /* 可选：添加阴影效果 */
  padding: 20px;
  /* 可选：添加一些内边距 */
  border: 1px solid #ebeef5;
  /* 根据你的截图，看起来你需要一个边框 */
}

.main {
  padding: 20px;
}

.back-button {
  position: absolute;
  top: 10px;
  left: 10px;
}

.button-container {
  /* This would right-align your button */
  text-align: right;
  /* Add other styles if needed */
}

.demo-table-expand {
  font-size: 0;
}

.demo-table-expand label {
  width: 90px;
  color: #99a9bf;
}

.demo-table-expand .el-form-item {
  margin-right: 0;
  margin-bottom: 0;
  width: 50%;
}

.three-times-answer.el-form-item {
  margin-right: 0;
  margin-bottom: 0;
  width: 100%;
}
</style>