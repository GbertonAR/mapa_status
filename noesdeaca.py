import React, { useState, useEffect, useMemo } from 'react';
// Importación corregida de botframework-webchat desde un CDN
// Se elimina la importación directa ya que se cargará globalmente
// import ReactWebChat, { createDirectLine, createStore } from 'https://esm.sh/botframework-webchat';

import { User, MapPin, Building, FileText, Share2, FormInput, Book, MessageSquare } from 'lucide-react'; // Iconos para los botones

// --- Configuración de Colores y Estilos (Basado en tus preferencias) ---
const accent_color = "#FFC107"; // Amarillo ámbar
const background_color = "#f0f8ff"; // Alice Blue (un azul muy claro)
const bot_avatar_bg = "#007bff"; // Azul primario
const user_avatar_bg = "#28a745"; // Verde éxitos

const custom_styles = {
  bubbleBackground: "#e0f7fa", // Azul claro para las burbujas del bot
  bubbleTextColor: "#1a237e", // Azul oscuro para el texto del bot
  userBubbleBackground: "#fffde7", // Amarillo muy claro para las burbujas del usuario
  userBubbleTextColor: "#4a148c", // Morado oscuro para el texto del usuario
  botAvatarImage: "https://placehold.co/40x40/007bff/ffffff?text=Bot", // Placeholder para el avatar del bot
  userAvatarImage: "https://placehold.co/40x40/28a745/ffffff?text=Yo", // Placeholder para el avatar del usuario
  typingAnimationBackgroundColor: "#ffeb3b", // Amarillo brillante para la animación de escritura
  sendButtonBackground: accent_color,
  sendButtonColor: "#fff",
  accent: accent_color, // Usado por Web Chat para ciertos elementos
  backgroundColor: background_color,
  // Fuentes personalizadas (asegúrate de que estén disponibles si no son estándar)
  fontFamily: 'Inter, sans-serif',
  // Estilos para burbujas y avatares
  bubbleBorderRadius: 12,
  bubbleFromUserBorderRadius: 12,
  avatarSize: 40,
  avatarBorderRadius: 20,
  // Estilos de la barra de entrada
  sendBoxButtonColor: accent_color,
  sendBoxButtonColorOnHover: '#e6b800', // Un poco más oscuro al pasar el ratón
  sendBoxBackground: '#ffffff',
  sendBoxTextColor: '#333333',
  sendBoxBorderRadius: 20,
  sendBoxHeight: 50,
  // Scrollbar
  rootScrollbarButtonColor: accent_color,
  rootScrollbarThumbColor: accent_color,
  rootScrollbarTrackColor: '#e0e0e0',
};

// --- Componente de Tarjeta de Perfil de Usuario ---
const UserProfileCard = ({ user }) => {
  return (
    <div className="bg-white p-6 rounded-xl shadow-lg m-4 w-full md:w-64 flex-shrink-0">
      <h2 className="text-2xl font-bold text-gray-800 mb-4 flex items-center">
        <User className="mr-2 text-blue-600" size={24} />
        Mi Perfil
      </h2>
      <div className="space-y-3 text-gray-700">
        <p className="flex items-center">
          <User className="mr-2 text-gray-500" size={18} />
          <span className="font-semibold">Nombre:</span> {user.name}
        </p>
        <p className="flex items-center">
          <MapPin className="mr-2 text-gray-500" size={18} />
          <span className="font-semibold">Provincia:</span> {user.province}
        </p>
        <p className="flex items-center">
          <Building className="mr-2 text-gray-500" size={18} />
          <span className="font-semibold">Municipio:</span> {user.municipality}
        </p>
      </div>
      <button className="mt-6 w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-lg transition duration-300 shadow-md">
        Editar Perfil
      </button>
    </div>
  );
};

// --- Componente de Botones del Menú Personalizados ---
const CustomMenuButtons = ({ buttons, dispatch }) => {
  const getIcon = (title) => {
    switch (title) {
      case "1. Obtener documentos": return <FileText size={20} />;
      case "2. Compartir documentos": return <Share2 size={20} />;
      case "3. Completar formularios": return <FormInput size={20} />;
      case "4. Biblioteca de documentos": return <Book size={20} />;
      case "5. Soporte en vivo": return <MessageSquare size={20} />;
      case "Salir": return <User size={20} />; // O un icono de salida
      default: return null;
    }
  };

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 p-4">
      {buttons.map((button, index) => (
        <button
          key={index}
          className="
            flex items-center justify-center space-x-2
            bg-gradient-to-r from-blue-500 to-purple-600
            hover:from-blue-600 hover:to-purple-700
            text-white font-bold py-3 px-6 rounded-full
            shadow-md hover:shadow-lg transition-all duration-300 ease-in-out
            transform hover:-translate-y-1
            focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-opacity-75
          "
          onClick={() => dispatch({ type: 'WEB_CHAT/SEND_MESSAGE', payload: { text: button.value } })}
        >
          {getIcon(button.title)}
          <span>{button.title.replace(/^\d+\.\s/, '')}</span> {/* Elimina el número y el punto */}
        </button>
      ))}
    </div>
  );
};

// --- Componente Principal de la Aplicación ---
const App = () => {
  const [directLine, setDirectLine] = useState(null);
  const [webChatStore, setWebChatStore] = useState(null);
  const [userProfile, setUserProfile] = useState({
    name: "Juan Pérez",
    province: "Buenos Aires",
    municipality: "La Plata",
  });
  // Nuevo estado para almacenar los componentes de Web Chat una vez cargados
  const [webChatComponents, setWebChatComponents] = useState(null); 

  // --- Reemplaza 'YOUR_DIRECT_LINE_SECRET_HERE' con tu clave de Direct Line de Azure ---
  const directLineSecret = "YOUR_DIRECT_LINE_SECRET_HERE"; 

  // Efecto para cargar el script de Web Chat dinámicamente
  useEffect(() => {
    const scriptId = 'botframework-webchat-script';
    // Si el script ya está en el DOM, no lo añadas de nuevo
    if (!document.getElementById(scriptId)) {
      const script = document.createElement('script');
      script.id = scriptId;
      script.src = 'https://cdn.botframework.com/botframework-webchat/latest/webchat.js';
      script.onload = () => {
        // Una vez que el script se carga, window.WebChat debería estar disponible
        if (window.WebChat) {
          setWebChatComponents({
            ReactWebChat: window.WebChat.ReactWebChat,
            createDirectLine: window.WebChat.createDirectLine,
            createStore: window.WebChat.createStore,
          });
        } else {
          console.error("Error: window.WebChat no está disponible después de cargar el script.");
        }
      };
      script.onerror = (e) => {
        console.error("Error cargando el script de Web Chat:", e);
      };
      document.body.appendChild(script);
    } else {
      // Si el script ya está presente (ej. en recargas en caliente), asegura que los componentes estén configurados
      if (window.WebChat) {
        setWebChatComponents({
          ReactWebChat: window.WebChat.ReactWebChat,
          createDirectLine: window.WebChat.createDirectLine,
          createStore: window.WebChat.createStore,
        });
      }
    }
  }, []); // Este efecto se ejecuta solo una vez al montar el componente

  // Efecto para inicializar Direct Line y el Store una vez que los componentes de Web Chat estén cargados
  useEffect(() => {
    if (webChatComponents && directLineSecret !== "YOUR_DIRECT_LINE_SECRET_HERE") {
      const { createDirectLine, createStore } = webChatComponents;

      const dl = createDirectLine({
        token: directLineSecret, // Usar el secreto directamente para desarrollo
      });

      setDirectLine(dl);

      const store = createStore();
      setWebChatStore(store);

      // Limpiar la conexión al desmontar el componente
      return () => {
        dl.end();
      };
    }
  }, [webChatComponents, directLineSecret]); // Depende de webChatComponents y directLineSecret

  // Middleware para personalizar la renderización de las actividades
  const activityMiddleware = useMemo(() => () => next => cardActivity => {
    const { activity } = cardActivity;

    // Detectar si es una actividad de mensaje con un HeroCard (que contiene botones)
    if (activity.type === 'message' && activity.attachments && activity.attachments.length > 0) {
      const heroCardAttachment = activity.attachments.find(
        att => att.contentType === 'application/vnd.microsoft.card.hero'
      );

      if (heroCardAttachment && heroCardAttachment.content && heroCardAttachment.content.buttons) {
        // Si es un HeroCard con botones, renderizamos nuestros botones personalizados
        return ({
          ...cardActivity,
          renderAttachments: () => (
            <div className="p-2">
              <p className="text-gray-700 text-lg mb-3 font-semibold">{heroCardAttachment.content.text || heroCardAttachment.content.title}</p>
              {/* Asegura que webChatStore esté disponible antes de pasar dispatch */}
              {webChatStore && <CustomMenuButtons buttons={heroCardAttachment.content.buttons} dispatch={webChatStore.dispatch} />}
            </div>
          ),
          // Opcional: Si quieres ocultar el texto original de la tarjeta, puedes modificar renderActivityStatus
          renderActivityStatus: () => null,
        });
      }
    }
    // Si no es un HeroCard con botones, dejar que Web Chat lo renderice normalmente
    return next(cardActivity);
  }, [webChatStore]); // Depende de webChatStore para acceder a dispatch

  // Muestra un mensaje de carga hasta que directLine y los componentes de Web Chat estén listos
  if (!directLine || !webChatComponents) { 
    return (
      <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-blue-700 to-indigo-900 text-white text-2xl">
        Cargando bot...
      </div>
    );
  }

  // Desestructura ReactWebChat una vez que webChatComponents está disponible
  const { ReactWebChat: LoadedReactWebChat } = webChatComponents; 

  return (
    <div className="font-inter flex flex-col md:flex-row h-screen overflow-hidden" style={{ backgroundColor: background_color }}>
      {/* Columna Izquierda: Tarjeta de Perfil */}
      <div className="w-full md:w-1/4 flex justify-center items-start pt-8 md:pt-16 bg-gray-50">
        <UserProfileCard user={userProfile} />
      </div>

      {/* Columna Derecha: Contenedor del Web Chat */}
      <div className="flex-1 flex flex-col p-4 md:p-8">
        <h1 className="text-3xl md:text-4xl font-extrabold text-gray-900 mb-6 text-center">
          Bienvenido a tu Asistente Inteligente
        </h1>
        <div className="flex-1 bg-white rounded-xl shadow-2xl overflow-hidden flex flex-col">
          {/* Asegura que webChatStore y LoadedReactWebChat estén disponibles antes de renderizar */}
          {webChatStore && LoadedReactWebChat && ( 
            <LoadedReactWebChat
              directLine={directLine}
              store={webChatStore}
              styleOptions={custom_styles}
              activityMiddleware={activityMiddleware}
              className="flex-1" // Asegura que el Web Chat ocupe el espacio disponible
            />
          )}
        </div>
      </div>
    </div>
  );
};

export default App;
