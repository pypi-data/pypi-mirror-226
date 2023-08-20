#include <string>
#include <iostream>
#include <sys/time.h>
using namespace std;
#if !defined(TXL_H)
#define TXL_H

///数据结构
struct dtm
{
  string name;
  string var;
  string channel;
};

class tx
{
public:
  ///数据中心接口提供登陆相关函数、数据中心相关函数、针对callback模式回调式广播函数set_callback与get_p
  ///若需要进行文件传输，请使用python下的getfile与sendfile函数
  ///性能模式选择
  virtual bool setp(bool var)=0;///用于选择性能模式: 不设置或者设置为true为轻量级模式；false为允许广播采用高性能模式。
  ///建立连接相关函数:
  
  virtual int creat_connect(string cip,int cpt,string tocken)=0;///指定连接的ip地址，端口，数据中心安全口令
 
  virtual int login()=0;///登陆函数，连接到数据中心
  
  virtual int login_lite()=0;///登陆函数，不加载广播功能，连接到数据中心

  virtual int login(string name)=0;///登陆函数，其中name为需要订阅的私有信号通道名称，多个name用@隔开，不填写代表不订阅私有信号通道的信息

  virtual int change_channel(string new_channel)=0;///支持在运行过程中对信道进行热切，参数是新的全部信道信息

  virtual int logout()=0;///断开并登出数据中心
  
  ///数据中心相关函数:
  
  virtual int put(string name,string var)=0;///给name变量赋值为var(带验证数据中心状态功能)
  
  virtual int put_lock(string name,string var,double time_out)=0;///提供put同时增加一把时间锁，本次赋值后的time_out秒内，该变量不能被修改；锁定期最大为10秒，超过10秒的只能锁10秒

  virtual string get(string name)=0;///获取变量name的值

  virtual int push_get(string name,string user_name)=0;///通过push_get将云变量冲刷下来，name是变慢名称，user_name是接收结果的信道
  
  virtual int del_d(string name)=0;///删除变量name

  virtual int putx(string name,string var)=0;///给name变量赋值为var(极速版，将数据赋值交给数据中心独立完成)
  
  virtual int push(string name,string var)=0;///向全域用户发送广播
  
  virtual int push(string name,string var,string user_name)=0;///向订阅了user_name私有信道的用户发送定向广播
  
  virtual int pushs(string name,string var)=0;///顺序推送函数，相对push而言,在大量push时通过牺牲少量性能(push函数为并发推送，用户收到消息的顺序可能与发送者不同)，保证接收者的数据顺序与推送者一致,方法同push
  
  virtual int pushs(string name,string var,string user_name)=0;///向订阅了user_name私有信道的用户发送定向顺序广播
  
  virtual int u_push(string name,string var)=0;///以UDP模块进行局域网广播,使用方法同push
  
  virtual int put_push(string name,string var)=0;///特定对象广播+赋值
  
  virtual int put_push(string name,string var,string user_name)=0;///特定对象广播+赋值，相当于push+putx
  
  virtual bool set_callback(bool iscallback)=0;///设置是否为callback模式下，若参数为true,则get_p函数启用，下方的"打印收到的广播"函数无效,默认为false;

  virtual string get_p(bool block=true)=0;///在设置set_callback(true)的情况下，本函数通过消息队列的方式替代下方"打印收到的广播"函数，block参数为true则为阻塞模式，false为非阻塞模式,默认为true;获取到的值组成方式为"id|变量名|变量值"

  virtual bool free_get_p(string var)=0;

  virtual string get_log_data(string name,long start_index,long end_index)=0;///获取名为name的日志，范围是从start_index个到第end_index个

  virtual long get_log_size(string name)=0;///获取名为name的日志包含的总日志条数

  virtual int append_log_data(string name,string var)=0;///向名为name的日志增加日志，内容为var；日志可以当成队列使用，在服务端存在磁盘中，而非内存中。

  virtual int del_log_data(string name)=0;///删除名为name的日志

  virtual int change_log_data(string name,long index,string var)=0;///修改名为name的日志的第index条内容为var

  virtual int get_lock(string name)=0;///获得一把名为name分布式锁

  virtual int release_lock(string name)=0;///释放一把名为name分布式锁

public:
  tx();
  ~tx();
};
#endif

///类指针快速创建函数，返回tx类指针。
tx* creat_api(int id);

///字符串分割：将s1按照s2分割；并返回分割好的第i个字符串(第一个的i为1)
string fg(string s1,string s2,int n);

///打印收到的广播，set_callback未设置为true的情况下，广播信息将通过该函数接收，否则应当通过get_p函数接收
void broadcast(dtm *pDtm, int id)
{
  cout<<"id:"<<id<<endl;///返回creat_api创建指针时输入的id,用于区分广播信息归属问题，默认0。归属问题也可以自行通过创建类的继承来实现区分。
  cout<<"name:"<<pDtm->name<<endl;///信息名称
  cout<<"var:"<<pDtm->var<<endl;///信息内容
  cout<<"var:"<<pDtm->channel<<endl;///信道名称
}

///打印收到的广播(UDP)，set_callback未设置为true的情况下，广播信息将通过该函数接收，否则应当通过get_p函数接收
void u_broadcast(dtm *pDtm, int id)
{
  cout<<"id:"<<id<<endl;///返回creat_api创建指针时输入的id,用于区分广播信息归属问题，默认0。归属问题也可以自行通过创建类的继承来实现区分。
  cout<<"name:"<<pDtm->name<<endl;///信息名称
  cout<<"var:"<<pDtm->var<<endl;///信息内容
}


///返回纳秒时间戳
long nm()
{
  struct timespec tn;
  clock_gettime(CLOCK_REALTIME, &tn);
  return tn.tv_sec*1000000000+tn.tv_nsec;
}
