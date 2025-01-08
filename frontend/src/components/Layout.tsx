import { Outlet } from 'react-router-dom';
import FamilyTreeDisplay from './FamilyTreeDisplay';

const Layout = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header with Title */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
          <h1 className="text-3xl font-bold text-gray-900">
            Mirasyedi: Inheritance Calculator
          </h1>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div className="bg-white shadow rounded-lg p-6">
            <Outlet />
          </div>
          <div className="bg-white shadow rounded-lg p-6">
            <FamilyTreeDisplay />
          </div>
        </div>
        
        {/* Legal Disclaimer */}
        <div className="mt-8 bg-gray-100 rounded-lg p-6 text-sm space-y-6">
          {/* Turkish Disclaimer - Placing Turkish first as it's the primary jurisdiction */}
          <div className="space-y-2">
            <h3 className="font-bold text-gray-900">Yasal Uyarı</h3>
            <p className="text-gray-700">
              İşbu miras hesaplama aracı ("Hesaplayıcı") kesinlikle ve yalnızca bilgilendirme amaçlı olup, hiçbir şekilde ve hiçbir koşulda hukuki tavsiye, görüş veya danışmanlık niteliği taşımamaktadır. Hesaplayıcı tarafından sunulan tüm hesaplamalar, sonuçlar ve bilgiler yaklaşık tahminlerden ibaret olup, hiçbir şekilde kesin, bağlayıcı veya yasal olarak geçerli belirlemeler olarak kabul edilemez.
            </p>
            <p className="text-gray-700">
              Hesaplayıcının kullanımı tamamen kullanıcının kendi sorumluluğunda olup, kullanıcı bu hesaplayıcıyı kullanarak tüm riskleri açıkça kabul etmiş sayılır. Hesaplayıcının kullanımından doğabilecek her türlü maddi ve manevi zarar, kayıp, masraf ve gider münhasıran kullanıcının sorumluluğundadır. Hesaplayıcı ve sağlanan bilgilerin doğruluğu, eksiksizliği, güncelliği, güvenilirliği, kullanılabilirliği veya belirli bir amaca uygunluğu konusunda hiçbir açık veya zımni garanti verilmemektedir.
            </p>
            <p className="text-gray-700">
              Miras hukuku son derece karmaşık, özel uzmanlık gerektiren ve her somut olayın kendine özgü koşullarının ayrıntılı olarak değerlendirilmesini gerektiren bir hukuk dalıdır. Hesaplayıcı üzerinden elde edilen sonuçlar, gerçek hukuki durumu yansıtmayabilir ve hiçbir şekilde hukuki işlemlere esas teşkil edemez. Bu nedenle, miras ile ilgili her türlü işlem ve karar için mutlaka ve istisnasız olarak konusunda uzman hukukçulara danışılması zorunludur.
            </p>
            <p className="text-gray-700">
              Hesaplayıcının kullanımı ile ortaya çıkabilecek doğrudan, dolaylı, arızi, özel, cezai veya sonuç olarak ortaya çıkan hiçbir zarar, veri kaybı, kâr kaybı, iş kaybı, itibar kaybı veya diğer her türlü kayıp ve zarardan hiçbir şekilde ve hiçbir koşulda sorumluluk kabul edilmeyecektir. Bu sorumluluk reddi, ilgili kayıp veya zararın olasılığından haberdar olunmuş olsa dahi geçerlidir.
            </p>
            <p className="text-gray-700">
              Mevzuatta meydana gelebilecek değişiklikler, yargı kararları, içtihatlar ve diğer her türlü düzenleme nedeniyle hesaplayıcıda yer alan bilgiler ve hesaplamalar güncelliğini yitirebilir. Bu durumdan kaynaklanabilecek her türlü hak kaybı, zarar veya olumsuz sonuçtan hiçbir şekilde sorumluluk kabul edilmemektedir.
            </p>
            <p className="text-gray-700">
              Hesaplayıcıyı kullanan kişiler, yukarıdaki tüm şartları ve uyarıları açıkça, gayrikabili rücu olarak kabul etmiş sayılırlar. Hesaplayıcının kullanımından doğabilecek her türlü ihtilaf Türkiye Cumhuriyeti kanunlarına tabidir. İşbu yasal uyarı metninin yorumlanmasında ve uygulanmasında Türk Hukuku geçerli olacaktır.
            </p>
          </div>

          {/* English Disclaimer */}
          <div className="space-y-2">
            <h3 className="font-bold text-gray-900">Legal Disclaimer</h3>
            <p className="text-gray-700">
              This inheritance calculator is provided for informational purposes only and does not constitute legal advice. The calculations and results provided by this tool are approximate estimations based on general principles of Turkish inheritance law and should not be considered as definitive legal determinations.
            </p>
            <p className="text-gray-700">
              While we strive to keep the information up to date and correct, we make no representations or warranties of any kind, express or implied, about the completeness, accuracy, reliability, suitability, or availability with respect to the calculator or the information provided. Any reliance you place on such information is therefore strictly at your own risk.
            </p>
            <p className="text-gray-700">
              For actual inheritance matters, we strongly recommend consulting with qualified legal professionals who can provide advice tailored to your specific situation. Inheritance laws are complex and may vary based on specific circumstances and changes in legislation.
            </p>
            <p className="text-gray-700">
              Under no circumstances shall we be liable for any loss or damage including without limitation, indirect or consequential loss or damage, or any loss or damage whatsoever arising from loss of data or profits arising out of, or in connection with, the use of this calculator.
            </p>
          </div>

          {/* Copyright Notice */}
          <div className="pt-4 border-t border-gray-200">
            <p className="text-gray-500 text-xs text-center">
              © {new Date().getFullYear()} Mirasyedi: Inheritance Calculator. All rights reserved. | Tüm hakları saklıdır.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Layout; 