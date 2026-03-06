# src/downloader.py
import os
import yt_dlp
import config  # Importamos la configuración para saber rutas

def descargar_video(url):
    """
    Descarga el video y extrae sus metadatos (likes, vistas, etc).
    Devuelve un diccionario con los stats o None si falla.
    """
    print(f"\n⬇️  Fase 1: DESCARGANDO: {url}")
    
    # Usamos un User-Agent genérico para que TikTok no nos bloquee
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    
    opciones = {
        'outtmpl': f'{config.NOMBRE_CRUDO}.%(ext)s', # Ruta desde config
        'format': 'best', 
        'quiet': True,
        'no_warnings': True,
        'overwrites': True,
        'cookiefile': config.COOKIES_PATH,
        'user_agent': user_agent,
        'http_headers': {'Referer': 'https://www.tiktok.com/'}
    }
    
    if not os.path.exists(config.COOKIES_PATH):
        print("⚠️ AVISO: Sin cookies. Los guardados (saves) saldrán a 0.")

    try:
        with yt_dlp.YoutubeDL(opciones) as ydl:
            # 1. Extraemos información
            info = ydl.extract_info(url, download=True)
            
            # 2. Intentamos buscar los "Guardados" (es el dato más difícil de sacar)
            guardados = info.get('favorite_count', 0)
            if guardados == 0 and 'stats' in info:
                guardados = info['stats'].get('favoriteCount', 0)
            if guardados == 0:
                try:
                    for entry in info.get('entries', []):
                         if 'favorite_count' in entry: guardados = entry['favorite_count']
                except: pass

            # 3. Empaquetamos los datos limpios
            stats = {
                'vistas': info.get('view_count', 0),
                'likes': info.get('like_count', 0),
                'guardados': guardados,
                'comentarios': info.get('comment_count', 0),
                'shares': info.get('repost_count', 0) or info.get('share_count', 0),
                'autor': info.get('uploader', 'Desconocido'),
                'duracion_meta': info.get('duration', 0)
            }
            print(f"   📊 DATOS: {stats['vistas']} Vistas | {stats['likes']} Likes | {stats['guardados']} Guardados")
            return stats

    except Exception as e:
        print(f"❌ Error descarga: {e}")
        return None