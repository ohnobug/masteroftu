import { CheckInfinityIcon } from "./icons/CheckInfinityIcon"
import { RocketIcon } from "./icons/RocketIcon"
import { CloudIcon } from "./icons/CloudIcon"
import { SlidersIcon } from "./icons/SlidersIcon"
import { ShieldIcon } from "./icons/ShieldIcon"
import { DevicesIcon } from "./icons/DevicesIcon"

const FeatureCard = ({ icon, title, children }) => (
  <div className="flex items-start space-x-4">
    <div className="flex-shrink-0">{icon}</div>
    <div>
      <h3 className="text-lg font-semibold text-dark-charcoal">{title}</h3>
      <p className="text-gray-600 mt-1">{children}</p>
    </div>
  </div>
);

const Features = () => (
  <div className="bg-white rounded-lg shadow-lg p-10 mt-12">
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-x-8 gap-y-12">
      <FeatureCard icon={<CheckInfinityIcon />} title="支持超过 300 种格式">
        我们支持超过 300 种不同的文件格式之间的转换。数量全面超越其他任何转换器。
      </FeatureCard>
      <FeatureCard icon={<RocketIcon />} title="快速简便">
        您只需将文件拖放至页面，选择输出格式并点击“转换”按钮即可。完成转换过程需要一点时间，请稍等。
      </FeatureCard>
      <FeatureCard icon={<CloudIcon />} title="云端处理">
        所有转换都在云端进行，不会消耗您计算机的资源。
      </FeatureCard>
      <FeatureCard icon={<SlidersIcon />} title="自定义设置">
        大多数转换类型都支持高级选项。例如，对于视频转换器，您可以选择质量、长宽比、编解码器及其他设置、旋转和翻转。
      </FeatureCard>
      <FeatureCard icon={<ShieldIcon />} title="安全保障">
        我们将立即删除已上传的文件，并在 24 小时后删除已转换的文件。任何人都无法访问您的文件，我们可确保您的隐私 100% 安全。
      </FeatureCard>
      <FeatureCard icon={<DevicesIcon />} title="支持所有设备">
        Convertio 基于浏览器并支持所有平台。您无需下载与安装任何软件。
      </FeatureCard>
    </div>
  </div>
);

export default Features;