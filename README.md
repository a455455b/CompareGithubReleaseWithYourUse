# CompareGithubReleaseWithYourUse
Check whether the latest version number of the project on the Github project is consistent with the version number of the local warehouse through the CI tool polling.

# Description
  A simple but necessary script that is executed periodically by the CI tool. By parsing the RSS link provided by github, it compares it with the repository configuration file that parses the local project. The example script parses the iOS pod file. Support multiple remote urls and multiple local library comparisons, the output can be notified to the team via slack/ifttt/robot.

  一个简单但是很有必要的脚本，通过CI工具定时执行。通过解析github提供的RSS链接，和通过解析本地项目的仓库配置文件作对比。实例脚本解析的是iOS的pod文件。支持多个远程url和多个本地库对比，输出的结果可以通过slack/ifttt/robot 来通知到团队。