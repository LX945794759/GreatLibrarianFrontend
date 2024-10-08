<template>
  <el-container style="height: 100vh;">
    <el-container>
      <!-- 主体部分 -->
      <el-main v-loading="loading">
        <el-row :gutter="20">
          <!-- 左侧项目列表区域 -->
          <el-col :span="18">
            <div class="project-section">
              <el-card shadow="hover" class="box-card">
                <div slot="header" class="clearfix">
                  <span style="float: left;">我创建的项目</span>
                  <el-link style="float: right;" @click="pushToProject()">我的项目列表</el-link>
                </div>
                <el-table :data="myProjects">
                  <!-- <el-table-column label="项目 ID" prop="id"></el-table-column> -->
                  <el-table-column label="项目名称" prop="name"></el-table-column>
                  <!-- <el-table-column label="测试说明" prop="info"></el-table-column> -->
                  <el-table-column label="LLM">
                    <template slot-scope="scope">
                      <div style="height: 70px; overflow-y: auto; display: flex; flex-direction: column;">
                      <div v-for="apiKey in scope.row.apiKey" :key="apiKey.id">
                        <!-- {{ apiKey.id }} - {{ apiKey.name }} -->
                        {{ apiKey.name }}
                      </div>
                      </div>
                    </template>
                  </el-table-column>

                  <!-- 数据集 列 -->
                  <el-table-column label="数据集">
                    <template slot-scope="scope">
                      <div style="height: 70px; overflow-y: auto; display: flex; flex-direction: column;">
                      <div v-for="data in scope.row.dataSet" :key="data.id">
                        <!-- {{ data.id }} - {{ data.name }} -->
                        {{ data.name }}
                        </div>
                      </div>
                    </template>
                  </el-table-column>
                  <el-table-column label="" prop="">
                    <template slot-scope="scope">
                      <el-link @click="handleExperiment(scope.row)" type="primary">测试列表</el-link>
                    </template>
                  </el-table-column>
                </el-table>
              </el-card>

              <el-card shadow="hover" class="box-card" style="margin-top: 20px;">
                <div slot="header" class="clearfix">
                  <span>我协助的测试</span>
                </div>
                <el-table :data="participatedExp">
                  <!-- 表格内容 -->
                  <!-- <el-table-column label="测试 ID" prop="id"></el-table-column> -->
                  <el-table-column label="测试名称" prop="name"></el-table-column>
                  <el-table-column label="待审核条数" prop="thisExpQA">
                    <template slot-scope="scope">
                      <el-tag type="warning">{{ scope.row.thisExpQA }}</el-tag>
                    </template>
                  </el-table-column>
                  <el-table-column label="" prop=""><el-link href="/experimentCollaborate"
                      type="primary">去审核</el-link></el-table-column>
                </el-table>
              </el-card>
            </div>
          </el-col>

          <!-- 下载链接 -->
          <!-- <el-button plain type="primary" @click="downloadFile()">下载文件</el-button> -->

          <!-- 右侧好友列表区域 -->
          <el-col :span="6">
            <el-badge :value="friendRequestNumebr" class="item" style="margin-top: 20px;">
              <el-button plain icon="el-icon-bell" size="large" @click="pushToFriendRequest">待处理的好友请求</el-button>
            </el-badge>
            <el-card shadow="hover" class="box-card">
              <div slot="header" class="clearfix">
                <span>我的好友</span>
              </div>
              <template v-if="userFriends&&userFriends.length">
                <div v-for="(friend, index) in userFriends" :key="index" class="friend">
                  <!-- <el-avatar :src="friend.icon"></el-avatar> -->
                  <img :src="friend.icon" style="width: 50px; height: 50px; border-radius: 50%;" class="friend-icon" @error="handleImageError" />
                  <div class="friend-info">
                    <span>{{ friend.name }}</span>
                  </div>
                </div>
              </template>
              <div v-else class="empty-friends">
                暂无好友
              </div>
            </el-card>
          </el-col>
        </el-row>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import { getUserList, getFriendsRequest } from "@/api/collaborate";
import { getExperimentsByUserId } from "@/api/collaborate"
import { getProjectsByUserId } from "@/api/project"
import { getQAByExpirenceId } from "@/api/qa"
import config from "@/services/conf"
export default {
  name: "userHome",
  data() {
    return {
      loading: true,
      defaultAvatar: require('@/assets/avatar.png'),
      userFriends: [],
      myProjects: [],
      participatedExp: [],
      friendRequestNumebr: 0
    }
  },
  methods: {
    load() {
      const uid = localStorage.getItem('uid')
      //获取好友列表
      getUserList(uid).then(res => {
        this.userFriends = res.data.filter(user => user.state === 1 || user.state === -1)
        this.userFriends = this.userFriends.map(user => {
          if (user.icon) {
            let icon = user.icon.replace(/\\/g, '/'); // 替换所有反斜杠为斜杠
            icon = icon.replace(/App/g, '');
            icon = config.API_URL + icon; // 拼接完整的 URL
            return { ...user, icon }; // 返回更新后的用户对象
          }
          else {
            return { ...user, icon: this.defaultAvatar };
          }
        });
      })
      //获取好友请求信息个数
      getFriendsRequest(uid).then(res => {
        // 假设 res.data 是从某个地方获得的数据
        if (res.fid.length)
          this.friendRequestNumebr = res.fid.length;

      })
      //获取项目信息
      getProjectsByUserId(uid).then(res => {
        this.myProjects = res.data
      })
      //获取参与的测试
        const id = localStorage.getItem("uid")
        getExperimentsByUserId(id).then(res => {
          this.participatedExp = res.data.filter(exp=>exp.status===2);
          Promise.all(this.participatedExp.map(exp => {
            // 对每个exp调用getQAByExpirenceId函数
            return getQAByExpirenceId(exp.id, localStorage.getItem('uid')).then(res => {
              // 将结果合并回exp对象
              return {
                ...exp,
                thisExpQA: res.data.length
              };
            });
          })).then(updatedExperimentList => {
            // 这里的updatedExperimentList包含了修改后的experimentList
            // 可以在这里处理或更新状态
            this.participatedExp = updatedExperimentList;
            console.log('我参与的测试', this.participatedExp)
          }).catch(error => {
            // 处理任何在Promise链中发生的错误
            console.error("Error while updating experiment list:", error);
          });
        })
    },
    //跳转处理好友请求
    pushToFriendRequest() {
      this.$router.push('/FriendRequests')
    },
    pushToProject() {
      this.$router.push('/projectsList')
    },
    handleExperiment(project) {
      console.log('该项目', project)
      if (project.apiKey.length === 0) {
        this.$message({
          message: '请重新配置API key',
          type: 'warning'
        });
        return
      }
      else if (project.dataSet.length === 0) {
        this.$message({
          message: '请重新配置数据集',
          type: 'warning'
        });
      }
      else {
        localStorage.setItem('thisProject', JSON.stringify(project));
        this.$router.push("/experimentList")
      }
    },
    handleImageError(event){
      event.target.src="https://cube.elemecdn.com/e/fd/0fc7d20532fdaf769a25683617711png.png"
    }
  },
  mounted() {
    setTimeout(() => {
      if (localStorage.getItem("uid") !== null) {
        this.load()
        setTimeout(() => {
          this.loading = false
        }, 300);
      }
        }, 600);
  },
}
</script>
<style scoped>
.friend {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
  /* 垂直居中 */
}

.friend-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin-right: 10px;
  /* 在图像和名字之间添加一些空间 */
}
</style>