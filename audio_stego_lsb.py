import wave, argparse

def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--input", required=True, help="Input for audio file to either decode or encode")
    parser.add_argument("-e", "--encode", help="Tell program you are encoding a message. If unused, it will try to decode a message", action='store_true')
    parser.add_argument("-o", "--output", help="Name of the output file if decoding. Program only functions with WAVE files, so only use *.wav files for output. Default value: output.wav")
    parser.add_argument("-m", "--message", metavar="", help="Type the message you wish to encode in the input audio file")
    args = parser.parse_args()

    #Set the variables to default values as if it was just going to decode a file
    output  = "output.wav"
    message = "default"
    input = args.input
    encode = False

    #Check if anything exists that mean a message should be encoded
    if args.output:
        output = args.output
    #If -m is given it implies -e even if it wasn't used so set encode to True
    if args.message:
        message = args.message
        encode = True
    if args.encode:
        encode = True

    #If we're encoding a message, tell them so
    if encode:
        print('File to encode message into : %s.' % input)
        print('Message encoded: %s' % message)
        print('Output file with encoded message: %s' % output)
    #If nothing changes, tell them a message is being decoded
    else:
        print('Decoding message from: %s' % input)

    return (input, output, message, encode)


def encode_decode(inpt, output, message, encode):

    if encode:
        #Open the input audio file and get the bytes from the file
        inpt_song = wave.open(inpt, mode='rb')#open the input audio file
        frame_bytes = bytearray(list(inpt_song.readframes(inpt_song.getnframes())))#Get the bytes from the input file

        #There might be extra bytes that arent going to be used so fill the message to fit every byte but make them '*' to act as placeholders
        full_message = message + int((len(frame_bytes)-(len(message)*8*8))/8) *'#'

        #Convert the message into bytes and convert it to just the bits
        bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in full_message])))

        #Now, add the byte form of the message into the audio file's byte at the least significant bit
        for i, bit in enumerate(bits):
            frame_bytes[i] = (frame_bytes[i]&254)|bit
        #Store the new mixed bytes that have the message in the LSB
        frame_modified = bytes(frame_bytes)

        #Get the parameters of the original song, then convert the encoded byte array into an audio file that fits those parameters
        with wave.open(output, 'wb') as fd:
            fd.setparams(inpt_song.getparams())
            fd.writeframes(frame_modified)
        inpt_song.close()

    else:
        inpt_song = wave.open(inpt, mode='rb')
        # Convert audio to byte array and open the input file
        frame_bytes = bytearray(list(inpt_song.readframes(inpt_song.getnframes())))

        # Get each least significant byte from the audio file
        extracted_bytes = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
        # Turn the bytes into a message
        message = "".join(chr(int("".join(map(str,extracted_bytes[i:i+8])),2)) for i in range(0,len(extracted_bytes),8))
        # Remove all the empty characters (When you have the full message, there's a bunch of ### to fill up space, so cut them out)
        decoded_message = message.split("###")[0]

        # Pirnt out the decoded message
        print("Decoded the message: "+decoded_message)
        inpt_song.close()


#Main that gets the arguments then either decodes or encodes a message
inpt = parser();
encode_decode(*inpt)
