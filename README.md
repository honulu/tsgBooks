# :books:命令行模式下的新书查询

- 使用`requests`,`beautifulsoup4`,`re`,`html.parser`库编写的命令行模式下查询学校图书馆新进了什么书
- 在wsl+terminal以及linux下可正常食用.

## :fork_and_knife:如何食用

- `linux`下

  1. 将主文件移动到`/usr/local/bin/`下来方便使用.

     ```shell
     $ sudo mv ./tsg  ./ tsgmain.py /usr/local/bin/
     ```

  2. 在命令行下键入`tsg`回车即可查询.

  

## :construction:计划是

- [x] 更好的显示

  - [x] 进度条
  - [x] 命令行标准输出

- [ ] 自动获取新书

- [ ] 新书提醒

- [x] 存储数据
  
  

## :tada:适用于

主要是针对齐齐哈尔大学图书馆写的, 如果你们学校图书馆用的也是汇文OPAC v5.5, 那么修改一下登陆地址,理论上可以直接用,如果有不适合的地方修改tsgmain.py就可以.
