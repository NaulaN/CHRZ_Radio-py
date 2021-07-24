from typing import Optional
import os, json, datetime, shutil



class FileManager( object ):

    def __init__( self ):

        self.path = lambda directory, file: os.path.join( directory, file )

        self.msg_error_read =  lambda file:    f"Les données n'ont pas pu êtres lu car le fichier { file } n'a pas étais trouvé !"
        self.msg_error_write = lambda file: f"Les données n'ont pas pu êtres ecrit car le fichier { file } n'a pas étais trouvé !"


    def load( self, file: str,
              directory: Optional[ str ]= os.getcwd() ):
        """ load( ) -> Load a file.
                :param file: Specify the name of your file with his extension.
                :param directory: Specify a directory to going access at your file. """
        name, extension = file.split( '.' )

        if extension == 'json':
            try:
                test_f = open( self.path( directory, file ) )
                test_f.close( )
            except FileNotFoundError:
                print( self.msg_error_read( file ) )
                return None
            finally:
                with open( self.path( directory, file ) ) as f:
                    data = json.load( f )
                    f.close( )
                return data


    def write( self, data, file: str,
               directory: Optional[ str ]= os.getcwd( ) ):
        """ write( ) -> Write a file.
                :param data: Specify a variable which contain your data at write.
                :param file: Specify the name of your file with his extension.
                :param directory: Specify a directory to going acces at your file. """
        name, extension = file.split( '.' )

        if extension == 'json':
            try:
                test_f = open( self.path( directory, file ) )
                test_f.close( )
            except FileNotFoundError:
                print( self.msg_error_write( file ) )
                return None
            finally:
                with open( self.path( directory, file ), 'w' ) as f:
                    json.dump( data, f )
                    f.close( )
                return data


    def copy( self, origin_dir: str, origin_file: str, backup_dir: str,
              backup_file: str= None ):
        """
            * Permet de copier un fichier correctement et simplement
                :param origin_dir: Le chemin d'accès original de votre fichier
                :param origin_file: Le nom de votre fichier d'origine
                :param backup_dir: Le chemin d'accès où le fichier copie va êtres
                :param backup_file: Le nom de votre fichier copie
        """
        # Si il y a pas de nom specifié
        if backup_file is None:
            date, hour = str( datetime.datetime.today( ) ).split( ' ' )
            h, m, s = hour.split( ':' )
            new_hour = f'{ h }-{ m }-{ round( float( s ) ) }'

            backup_file = f'{ origin_file }[{ date }_{ new_hour }]'

        origin_file_path = os.path.join( origin_dir, origin_file)
        backup_file_path = os.path.join( backup_dir, backup_file )

        # Crée le fichier
        with open( backup_file_path, 'x' ) as f:
            shutil.copy( origin_file_path, backup_file_path )
            f.close( )
