unit main;

{$mode objfpc}{$H+}

interface

uses
  Classes, SysUtils, Forms, Controls, Graphics, Dialogs,
  StdCtrls, ExtCtrls, LCLIntf, LCLType, RTTICtrls, Process, Clipbrd, fphttpclient;

type

  { TForm1 }

  TForm1 = class(TForm)
    Button1: TButton;
    Button2: TButton;
    Image1: TImage;
    Image4: TImage;
    Label1: TLabel;
    SaveDialog1: TSaveDialog;
    procedure Button1Click(Sender: TObject);
    procedure Button2Click(Sender: TObject);
    procedure FormCreate(Sender: TObject);
    procedure Image4MouseDown(Sender: TObject; Button: TMouseButton;
      Shift: TShiftState; X, Y: Integer);
    procedure Image4MouseMove(Sender: TObject; Shift: TShiftState; X, Y: Integer
      );
    procedure Image4MouseUp(Sender: TObject; Button: TMouseButton;
      Shift: TShiftState; X, Y: Integer);
  private

  public

  end;

var
  Form1: TForm1;

implementation
type
  TConfig = record
    mode: string;
    x: integer;
    y: integer;
  end;
var
  output: ansistring;
  img, bmp: TBitmap;
  background: TBitmap;
  config: TConfig;


{$R *.lfm}

{ TForm1 }

procedure writefile(fnam: string; txt: string);
var
  strm: TFileStream;
  n: longint;
begin
  strm := TFileStream.Create(fnam, fmCreate);
  n := Length(txt);
  try
    strm.Position := 0;
    strm.Write(txt[1], n);
  finally
    strm.Free;
  end;
end;

procedure TForm1.FormCreate(Sender: TObject);
begin
  WindowState := wsFullScreen;
  DeleteFile('/tmp/augscreen.bmp');
  RunCommand('import -window root /tmp/augscreen.bmp',output);
  img := TBitmap.Create;
  bmp := TBitmap.Create;
  background := TBitmap.Create;
  img.LoadFromFile('/tmp/augscreen.bmp');

  if not FileExists('/tmp/gray.bmp') then
    writefile('/tmp/gray.bmp',TFPHTTPClient.SimpleGet('https://raw.githubusercontent.com/Augmeneco/augscreenshoter/master/gray.bmp'));

  background.LoadFromFile('/tmp/gray.bmp');
  Image1.Width := Screen.Width;
  Image1.Height := Screen.Height;
  Image1.Canvas.Draw(0,0,img);
  Image1.Canvas.Brush.Style := bsClear;
  Image1.Canvas.Pen.Width :=3;
  Image1.Canvas.Pen.Color := RGBToColor(74,74,74);
  Image4.Left:=0;
  Image4.Top:=0;
  Image4.Width:=Screen.Width;
  Image4.Height:=Screen.Height;
end;

procedure TForm1.Button1Click(Sender: TObject);
begin
  //Clipboard.Assign(bmp);
  bmp.SaveToFile('/tmp/augscreen.bmp');
  RunCommand('xclip -selection clipboard -t image/bmp -i /tmp/augscreen.bmp',output);
  halt;
end;

procedure TForm1.Button2Click(Sender: TObject);
begin
  SaveDialog1.Title := 'Save screenshot';
  SaveDialog1.InitialDir := GetCurrentDir;
  SaveDialog1.Filter := 'PNG|*.png|JPEG|*.jpg|BMP|*.bmp';
  SaveDialog1.DefaultExt := 'png';
  SaveDialog1.FilterIndex := 1;
  if SaveDialog1.Execute then
    bmp.SaveToFile(SaveDialog1.FileName);
  SaveDialog1.Free;
  halt;
end;

procedure TForm1.Image4MouseDown(Sender: TObject; Button: TMouseButton;
  Shift: TShiftState; X, Y: Integer);
begin
  if button = mbLeft then
  begin
    label1.show;
    config.mode := 'move';
    config.x := x;
    config.y := y;
    Button1.Visible := False;
    Button2.Visible := False;
  end;
end;

procedure TForm1.Image4MouseMove(Sender: TObject; Shift: TShiftState; X,
  Y: Integer);
begin
  if config.mode = 'move' then
  begin
    Label1.Left:=config.x;
    Label1.Top:=config.y-label1.Height;
    Label1.Caption:=format('%dx%d',[x-config.x,y-config.y]);
    Image1.Canvas.Draw(0,0,img);
    Image1.Canvas.Rectangle(config.x,config.y,x,y);
  end;
end;

procedure TForm1.Image4MouseUp(Sender: TObject; Button: TMouseButton;
  Shift: TShiftState; X, Y: Integer);
var
  rect1, rect2: TRect;
begin
    if button = mbLeft then
    begin

      config.mode := 'stop';

      Button1.Visible := True;
      Button2.Visible := True;
      if (x+button1.Width > screen.Width) or (y+button1.Height > screen.Height) then
      begin
        Button1.Left := x-Button1.Width;
        Button1.Top := y-(Button1.Height*2)-2;

        Button2.Left := x-Button2.Width;
        Button2.Top := y-Button2.Height;
      end
      else
      begin
        Button1.Left := x;
        Button1.Top := y-Button1.Height-2;

        Button2.Left := x;
        Button2.Top := y;
      end;

      with rect1 do begin
        Left:=0;
        Top:=0;
        Right:=x-config.x;
        Bottom:=y-config.y;
      end;

      with rect2 do begin
        Left:=config.x;
        Top:=config.y;
        Right:=x;
        Bottom:=y;
      end;

      bmp.Width:=x-config.x;
      bmp.Height:=y-config.y;

      Image1.Canvas.Draw(0,0,img);
      bmp.Canvas.CopyRect(rect1, Image1.Canvas, rect2);

      image1.Canvas.StretchDraw(rect(0,0,screen.Width,screen.Height),background);
      image1.canvas.Draw(config.x,config.y,bmp);
      Image1.Canvas.Rectangle(config.x,config.y,x,y);

    end;
end;

end.

